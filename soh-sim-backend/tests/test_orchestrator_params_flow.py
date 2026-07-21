"""
SOH-SIM Orchestrator Params Flow 测试

验证编排器 (run_full_workflow) 正确传递所有新参数通过完整流水线。
"""

import json
import os
import uuid

import pytest

# 必须在导入 app 前设置
os.environ.setdefault("TEST_DATABASE_URI", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-orchestrator-params-2026")
os.environ.setdefault("CORS_ORIGINS", "*")

from app import app as _app  # noqa: E402
from database import Tenant, User, db  # noqa: E402
from routes.auth import generate_token, hash_password  # noqa: E402

# ==================== Fixtures ====================


@pytest.fixture(scope="session")
def app():
    """Session-scoped Flask app with in-memory DB."""
    with _app.app_context():
        db.create_all()
    yield _app


@pytest.fixture()
def client(app):
    """Unauthenticated test client."""
    with app.test_client() as c:
        yield c


@pytest.fixture()
def db_session(app):
    """Per-test DB session with SAVEPOINT rollback."""
    connection = db.engine.connect()
    transaction = connection.begin()
    try:
        yield db.session
    finally:
        transaction.rollback()
        connection.close()
        db.session.remove()


@pytest.fixture()
def seed_tenant(db_session):
    """Ensure default tenant exists."""
    tid = "00000000-0000-0000-0000-000000000001"
    t = db_session.get(Tenant, tid)
    if not t:
        t = Tenant(id=tid, name="Default Tenant", code="default", status="active")
        db_session.add(t)
        db_session.flush()
    return t


@pytest.fixture()
def seed_engineer(db_session, seed_tenant):
    """Create a test engineer user."""
    uid = str(uuid.uuid4())
    username = f"eng_{uid[:8]}"
    user = User(
        id=uid,
        tenant_id=seed_tenant.id,
        username=username,
        email=f"{username}@test.com",
        password_hash=hash_password("testpass123"),
        role="solution_engineer",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    return {"id": uid, "username": username, "role": "solution_engineer"}


@pytest.fixture()
def auth_headers_eng(seed_engineer):
    """Auth headers for engineer user."""
    token = generate_token(seed_engineer["id"])
    return {"Authorization": f"Bearer {token}"}


# ==================== Helper Functions ====================


def _post(client, url, data, headers=None):
    """Convenience POST helper."""
    h = headers or {}
    return client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
        headers=h,
    )


def _get(client, url, headers=None):
    """Convenience GET helper."""
    h = headers or {}
    return client.get(url, headers=h)


def _assert_success(resp, status=200):
    """Assert response is successful and return parsed JSON data."""
    acceptable = status if isinstance(status, tuple) else (status,)
    assert (
        resp.status_code in acceptable
    ), f"Expected {acceptable}, got {resp.status_code}: {resp.get_data(as_text=True)[:500]}"
    body = resp.get_json()
    assert body is not None, "Response is not valid JSON"
    assert body.get("success") is True, f"success=False: {body.get('error', body.get('message', 'unknown'))}"
    return body.get("data", body)


# ==================== Standard Survey Params ====================

SURVEY_PARAMS = {
    "ratedEnergy": 100,
    "totalPower": 50,
    "duration": 2,
    "temperature": 25,
    "cyclesPerDay": 1,
    "dod": 90,
    "cRate": 0.5,
    "requiredEnergy": 240,
    "location": "china",
}


# ==================== Test Class ====================


class TestOrchestratorParamsFlow:
    """Verify the orchestrator (run_full_workflow) correctly passes all new
    parameters through the full pipeline."""

    def test_workflow_passes_aux_params(self, client, auth_headers_eng):
        """POST /api/workflow/full with survey_params containing
        auxPowerMode='thermal', ambientTemp=32, coolingType='liquid'.
        Verify the returned recommendation.simulation exists and has valid data."""
        resp = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": {
                    **SURVEY_PARAMS,
                    "auxPowerMode": "thermal",
                    "ambientTemp": 32,
                    "coolingType": "liquid",
                },
                "strategy": "economic",
                "target_metric": "lcos",
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        recommendation = data.get("recommendation")
        assert recommendation is not None, "Recommendation should not be None"
        assert isinstance(recommendation, dict), f"recommendation should be a dict, got {type(recommendation)}"

        sim = recommendation.get("simulation")
        assert sim is not None, "Recommendation should have simulation data"
        assert "soh" in sim, "Simulation missing soh"
        assert "rte" in sim, "Simulation missing rte"
        assert "totalAcUsable" in sim, "Simulation missing totalAcUsable"
        assert (
            len(sim["totalAcUsable"]) == 26
        ), f"totalAcUsable should have 26 elements, got {len(sim['totalAcUsable'])}"

    def test_workflow_passes_efficiency_factors_none(self, client, auth_headers_eng):
        """POST /api/workflow/full with survey_params containing
        efficiencyFactors=None and degradation containing custom rte.
        Verify the recommendation.simulation.rte reflects custom values."""
        custom_rte = [88.5] * 26
        custom_soh = [98.0] * 26

        resp = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": {
                    **SURVEY_PARAMS,
                    "efficiencyFactors": None,
                },
                "strategy": "economic",
                "target_metric": "lcos",
                "degradation": {
                    "soh": custom_soh,
                    "rte": custom_rte,
                    "dod": [90.0] * 26,
                    "augQty": [0] * 26,
                },
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        recommendation = data.get("recommendation")
        assert recommendation is not None, "Recommendation should not be None"

        sim = recommendation.get("simulation")
        assert sim is not None, "Recommendation should have simulation data"

        # With efficiencyFactors=None, efficiencyCurves should be None
        # and rte should reflect custom values
        result_rte = sim.get("rte", [])
        assert len(result_rte) == 26, f"Expected 26 rte values, got {len(result_rte)}"

        # When efficiencyFactors=None, rte values should be close to the custom values
        # (they may be adjusted by chain-derived values, but should be within ~15%)
        for i in range(26):
            assert (
                abs(result_rte[i] - custom_rte[i]) < 15.0
            ), f"Year {i}: rte should be close to {custom_rte[i]}, got {result_rte[i]}"

    def test_workflow_cambodia_project(self, client, auth_headers_eng):
        """POST with Cambodia-like params: ratedEnergy=5, totalPower=250,
        duration=2, temperature=32, cyclesPerDay=1, dod=90, requiredEnergy=382,
        location='cambodia', auxPowerMode='thermal', ambientTemp=32,
        coolingType='liquid'. Verify recommendation exists with valid simulation
        and financial data."""
        cambodia_params = {
            "ratedEnergy": 5,
            "totalPower": 250,
            "duration": 2,
            "temperature": 32,
            "cyclesPerDay": 1,
            "dod": 90,
            "cRate": 0.5,
            "requiredEnergy": 382,
            "location": "cambodia",
            "auxPowerMode": "thermal",
            "ambientTemp": 32,
            "coolingType": "liquid",
        }

        resp = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": cambodia_params,
                "strategy": "economic",
                "target_metric": "lcos",
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        # Verify solutions exist
        solutions = data.get("solutions", [])
        assert len(solutions) >= 1, f"Expected >=1 solutions, got {len(solutions)}"

        recommendation = data.get("recommendation")
        assert recommendation is not None, "Recommendation should not be None"

        # Verify simulation data
        sim = recommendation.get("simulation")
        assert sim is not None, "Recommendation should have simulation data"
        assert len(sim.get("totalAcUsable", [])) == 26, "Simulation should have 26-year totalAcUsable"

        # Verify financial data
        fin = recommendation.get("financial")
        assert fin is not None, "Recommendation should have financial data"
        metrics = fin.get("metrics", {})
        assert "lcos" in metrics or "projectIrr" in metrics, "Financial should have metrics"

    def test_workflow_recommendation_structure(self, client, auth_headers_eng):
        """POST /api/workflow/full with standard params.
        Verify recommendation contains design, simulation, financial sub-objects.
        Verify design has containerQty, pcsQty.
        Verify simulation has soh, rte, totalAcUsable.
        Verify financial has metrics."""
        resp = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": SURVEY_PARAMS,
                "strategy": "economic",
                "target_metric": "lcos",
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        recommendation = data.get("recommendation")
        assert recommendation is not None, "Recommendation should not be None"
        assert isinstance(recommendation, dict), f"recommendation should be dict, got {type(recommendation)}"

        # Design
        design = recommendation.get("design")
        assert design is not None, "Recommendation missing design"
        assert isinstance(design, dict), f"design should be dict, got {type(design)}"
        assert "containerQty" in design, "Design missing containerQty"
        assert "pcsQty" in design, "Design missing pcsQty"
        assert isinstance(design["containerQty"], (int, float)), "containerQty should be numeric"
        assert design["containerQty"] > 0, "containerQty should be positive"

        # Simulation
        sim = recommendation.get("simulation")
        assert sim is not None, "Recommendation missing simulation"
        assert isinstance(sim, dict), f"simulation should be dict, got {type(sim)}"
        assert "soh" in sim, "Simulation missing soh"
        assert "rte" in sim, "Simulation missing rte"
        assert "totalAcUsable" in sim, "Simulation missing totalAcUsable"
        assert (
            len(sim["totalAcUsable"]) == 26
        ), f"totalAcUsable should have 26 elements, got {len(sim['totalAcUsable'])}"

        # Financial
        fin = recommendation.get("financial")
        assert fin is not None, "Recommendation missing financial"
        assert isinstance(fin, dict), f"financial should be dict, got {type(fin)}"
        assert "metrics" in fin, "Financial missing metrics"
        metrics = fin["metrics"]
        assert isinstance(metrics, dict), f"metrics should be dict, got {type(metrics)}"
        assert "projectIrr" in metrics or "irr" in metrics, "Financial metrics missing IRR"
        assert "lcos" in metrics or "lcoe" in metrics, "Financial metrics missing LCOS"

    def test_workflow_solutions_sorted(self, client, auth_headers_eng):
        """POST with target_metric='lcos'. Verify solutions are sorted
        (first solution should have the lowest score/lcos)."""
        resp = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": SURVEY_PARAMS,
                "strategy": "economic",
                "target_metric": "lcos",
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        solutions = data.get("solutions", [])
        assert len(solutions) >= 1, f"Expected >=1 solutions, got {len(solutions)}"

        # Verify scores are non-decreasing (sorted ascending for lcos)
        scores = []
        for sol in solutions:
            score = sol.get("score")
            if score is not None:
                scores.append(score)

        if len(scores) >= 2:
            for i in range(1, len(scores)):
                # LCOS scores should be sorted ascending (lower is better)
                if scores[i] != float("inf") and scores[i - 1] != float("inf"):
                    assert (
                        scores[i - 1] <= scores[i]
                    ), f"Solutions should be sorted by lcos: {scores[i-1]} > {scores[i]}"

        # First solution should be the recommendation
        recommendation = data.get("recommendation")
        if recommendation is not None and len(solutions) > 0:
            rec_score = recommendation.get("score")
            first_score = solutions[0].get("score")
            if rec_score is not None and first_score is not None:
                assert rec_score == first_score, "Recommendation should be the first (best) solution"

    def test_design_to_system_params_mapping(self):
        """Import _design_to_system_params from services.orchestrator.
        Call it with a design dict and survey_params containing
        auxPowerMode/ambientTemp/coolingType/efficiencyFactors.
        Verify all fields are present in the returned system_params."""
        from services.orchestrator import _design_to_system_params

        design = {
            "container": {"ratedEnergyMWh": 5},
            "pcs": {"ratedPowerMW": 2.5},
            "containerQty": 10,
            "pcsQty": 10,
            "duration": 2,
            "efficiencyChain": {"systemRTE": 97.5},
            "auxPower": {"bessAuxRun": 15.0, "bessAuxStandby": 2.5, "pcsAuxRun": 5.0, "pcsAuxStandby": 0.8},
        }

        survey_params = {
            "cyclesPerDay": 1,
            "temperature": 25,
            "dod": 90,
            "cRate": 0.5,
            "auxPowerMode": "thermal",
            "ambientTemp": 35,
            "coolingType": "air",
            "efficiencyFactors": None,
            "requiredEnergy": 300,
        }

        result = _design_to_system_params(design, survey_params)

        # Verify all expected fields
        assert result["ratedEnergy"] == 5
        assert result["initContainerQty"] == 10
        assert result["initPcsQty"] == 10
        assert result["duration"] == 2
        assert result["cyclesPerDay"] == 1
        assert result["temperature"] == 25
        assert result["dod"] == 90
        assert result["cRate"] == 0.5
        assert result["acEfficiency"] == 97.5
        assert result["bessAuxRun"] == 15.0
        assert result["bessAuxStandby"] == 2.5
        assert result["pcsAuxRun"] == 5.0
        assert result["pcsAuxStandby"] == 0.8
        assert result["auxPowerMode"] == "thermal"
        assert result["ambientTemp"] == 35
        assert result["coolingType"] == "air"
        assert result["efficiencyFactors"] is None
        assert result["requiredEnergy"] == 300

    def test_workflow_different_strategies(self, client, auth_headers_eng):
        """POST with strategy='economic' vs strategy='balanced'.
        Verify both return valid results (may have different designs)."""
        # Economic strategy
        resp_econ = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": SURVEY_PARAMS,
                "strategy": "economic",
                "target_metric": "lcos",
            },
            auth_headers_eng,
        )
        data_econ = _assert_success(resp_econ)

        # Balanced strategy
        resp_bal = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": SURVEY_PARAMS,
                "strategy": "balanced",
                "target_metric": "lcos",
            },
            auth_headers_eng,
        )
        data_bal = _assert_success(resp_bal)

        # Both should have solutions
        assert len(data_econ.get("solutions", [])) >= 1, "Economic strategy should have solutions"
        assert len(data_bal.get("solutions", [])) >= 1, "Balanced strategy should have solutions"

        # Both should return the strategy name
        assert data_econ.get("strategy") == "economic"
        assert data_bal.get("strategy") == "balanced"

        # Both recommendations should have valid data
        rec_econ = data_econ.get("recommendation")
        rec_bal = data_bal.get("recommendation")
        assert rec_econ is not None, "Economic recommendation should not be None"
        assert rec_bal is not None, "Balanced recommendation should not be None"

        # Both should have simulation with 26 years
        assert len(rec_econ.get("simulation", {}).get("totalAcUsable", [])) == 26
        assert len(rec_bal.get("simulation", {}).get("totalAcUsable", [])) == 26

    def test_workflow_error_on_missing_params(self, client, auth_headers_eng):
        """POST /api/workflow/full with empty survey_params.
        Verify returns 400 error."""
        resp = _post(
            client,
            "/api/workflow/full",
            {
                "survey_params": {},
            },
            auth_headers_eng,
        )
        assert resp.status_code == 400, f"Expected 400 for empty survey_params, got {resp.status_code}"

        body = resp.get_json()
        assert body is not None, "Response should be valid JSON"
        assert body.get("success") is False, "Response should indicate failure for empty survey_params"
