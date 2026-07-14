"""
SOH-SIM Efficiency Factors Null 测试

验证当 efficiencyFactors=None 时，流水线使用自定义 RTE 数组而非 10 因子链。
同时验证默认行为（FACTOR_DEFAULTS 使用链式效率计算）。
"""

import json
import os
import uuid

import pytest

# 必须在导入 app 前设置
os.environ.setdefault("TEST_DATABASE_URI", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-efficiency-factors-null-2026")
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


class TestEfficiencyFactorsNull:
    """Verify that when efficiencyFactors=None, the pipeline uses custom RTE arrays
    instead of the 10-factor chain. Also verify default behavior."""

    def test_null_factors_uses_custom_rte(self):
        """Call calculate_energy_accounting with efficiency_factors=None, and provide
        custom rte=[86.5]*26. Verify that cycle_rte uses 0.865 (86.5/100),
        NOT the FACTOR_DEFAULTS chain value."""
        from services.pipeline import FACTOR_DEFAULTS, calculate_energy_accounting

        params = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "acEfficiency": 100.0,  # No AC loss to isolate RTE
            "requiredEnergy": 200,
        }
        soh = [100.0] * 26
        rte = [86.5] * 26
        dod = [90.0] * 26
        aug_qty = [0] * 26

        result_null = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=None)

        # With None, cycle_rte = c_rte * ac_efficiency = (86.5/100) * 1.0 = 0.865
        expected_cycle_rte = 0.865
        expected_init_gross_year0 = (
            params["ratedEnergy"] * params["initContainerQty"] * (dod[0] / 100) * expected_cycle_rte * (soh[0] / 100)
        )
        # 5 * 10 * 0.9 * 0.865 * 1.0 = 38.925
        assert (
            abs(result_null["initGross"][0] - expected_init_gross_year0) < 0.01
        ), f"Expected initGross[0] ~ {expected_init_gross_year0}, got {result_null['initGross'][0]}"

        # Verify it's NOT using chain RTE
        # With FACTOR_DEFAULTS chain, cycle_rte would be different
        result_default = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=FACTOR_DEFAULTS)
        assert (
            abs(result_null["initGross"][0] - result_default["initGross"][0]) > 0.01
        ), "Null factors should produce different initGross than FACTOR_DEFAULTS"

    def test_default_factors_uses_chain(self):
        """Call calculate_energy_accounting with efficiency_factors=FACTOR_DEFAULTS.
        Verify it produces different results than with None."""
        from services.pipeline import FACTOR_DEFAULTS, calculate_energy_accounting

        params = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "acEfficiency": 100.0,
            "requiredEnergy": 200,
        }
        soh = [95.0] * 26
        rte = [90.0] * 26
        dod = [90.0] * 26
        aug_qty = [0] * 26

        result_default = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=FACTOR_DEFAULTS)
        result_null = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=None)

        # They should differ because chain RTE != custom RTE
        assert (
            result_default["initGross"][0] != result_null["initGross"][0]
        ), "Default factors and None should produce different initGross"

        # With FACTOR_DEFAULTS, the chain computes RTE from 10-factor product,
        # which is different from simple 90.0/100
        assert result_default["totalAcUsable"][0] > 0, "Default factors should produce valid totalAcUsable"
        assert result_null["totalAcUsable"][0] > 0, "Null factors should produce valid totalAcUsable"

    def test_null_factors_with_different_rte_per_year(self):
        """Use rte values that vary by year: [86.5, 86.4, 86.3, ...].
        Verify each year's init_gross reflects the corresponding rte value."""
        from services.pipeline import calculate_energy_accounting

        params = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "acEfficiency": 100.0,
            "requiredEnergy": 200,
        }
        soh = [100.0] * 26
        rte = [86.5 - 0.1 * i for i in range(26)]  # 86.5, 86.4, 86.3, ...
        dod = [90.0] * 26
        aug_qty = [0] * 26

        result = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=None)

        # Each year's initGross should reflect that year's RTE
        for i in range(26):
            expected_rte = (86.5 - 0.1 * i) / 100.0
            expected_gross = (
                params["ratedEnergy"] * params["initContainerQty"] * (dod[i] / 100) * expected_rte * (soh[i] / 100)
            )
            assert (
                abs(result["initGross"][i] - expected_gross) < 0.02
            ), f"Year {i}: expected initGross ~ {expected_gross}, got {result['initGross'][i]}"

        # Verify monotonic decrease
        for i in range(1, 26):
            assert (
                result["initGross"][i] <= result["initGross"][i - 1]
            ), f"Year {i}: initGross should not increase with decreasing RTE"

    def test_calculate_full_pipeline_null_factors(self):
        """Call calculate_full_pipeline with system_params containing
        "efficiencyFactors": None and degradation containing custom soh and rte
        arrays. Verify the result's rte matches the custom values (not chain-derived)."""
        from services.pipeline import NUM_YEARS, calculate_full_pipeline

        system_params = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "temperature": 25,
            "dod": 90,
            "cRate": 0.5,
            "acEfficiency": 100.0,
            "requiredEnergy": 200,
            "efficiencyFactors": None,
        }

        custom_rte = [86.5] * NUM_YEARS
        custom_soh = [100.0 - 0.5 * i for i in range(NUM_YEARS)]

        degradation = {
            "soh": custom_soh,
            "rte": custom_rte,
            "dod": [90.0] * NUM_YEARS,
            "augQty": [0] * NUM_YEARS,
        }

        result = calculate_full_pipeline(system_params, degradation=degradation)

        # With efficiencyFactors=None, efficiencyCurves should be None
        assert result["efficiencyCurves"] is None, "efficiencyCurves should be None when efficiencyFactors is None"
        assert result["efficiencyDetail"] is None, "efficiencyDetail should be None when efficiencyFactors is None"

        # rte should match custom values (since no chain overrides them)
        for i in range(NUM_YEARS):
            assert (
                abs(result["rte"][i] - custom_rte[i]) < 0.01
            ), f"Year {i}: rte should be custom value {custom_rte[i]}, got {result['rte'][i]}"

    def test_calculate_full_pipeline_default_factors(self):
        """Without efficiencyFactors key (or with FACTOR_DEFAULTS). Verify rte
        comes from chain."""
        from services.pipeline import FACTOR_DEFAULTS, NUM_YEARS, calculate_full_pipeline

        system_params = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "temperature": 25,
            "dod": 90,
            "cRate": 0.5,
            "acEfficiency": 100.0,
            "requiredEnergy": 200,
            # efficiencyFactors key ABSENT — should default to FACTOR_DEFAULTS
        }

        degradation = {
            "soh": [95.0] * NUM_YEARS,
            "rte": [90.0] * NUM_YEARS,
            "dod": [90.0] * NUM_YEARS,
            "augQty": [0] * NUM_YEARS,
        }

        result = calculate_full_pipeline(system_params, degradation=degradation)

        # With default factors, efficiencyCurves should NOT be None
        assert result["efficiencyCurves"] is not None, "efficiencyCurves should not be None with default factors"
        assert result["efficiencyDetail"] is not None, "efficiencyDetail should not be None with default factors"

        # rte should come from chain (not raw 90.0)
        # Chain RTE for SOH=95 should differ from 90.0
        chain_rte = result["rte"]
        for i in range(NUM_YEARS):
            # Chain RTE is typically around 90-93% based on the 10-factor product
            assert chain_rte[i] > 0, f"Year {i}: chain rte should be positive"

        # Verify it's different from raw rte (the chain overrides it)
        raw_rte = degradation["rte"]
        # At least some years should differ
        differs = any(abs(chain_rte[i] - raw_rte[i]) > 0.5 for i in range(NUM_YEARS))
        assert differs, "Chain RTE should differ from raw RTE when using default factors"

    def test_null_factors_ac_efficiency_still_applied(self):
        """With efficiencyFactors=None and acEfficiency=100.0, verify
        cycle_rte = custom_rte_value/100 (no double-dipping on AC losses)."""
        from services.pipeline import calculate_energy_accounting

        params = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "acEfficiency": 100.0,  # 100% — no additional AC loss
            "requiredEnergy": 200,
        }
        soh = [100.0] * 26
        rte = [85.0] * 26
        dod = [90.0] * 26
        aug_qty = [0] * 26

        result = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=None)

        # cycle_rte = c_rte * ac_efficiency = 0.85 * 1.0 = 0.85
        # initGross = 5 * 10 * 0.9 * 0.85 * 1.0 = 38.25
        expected_gross = 5 * 10 * 0.9 * 0.85 * 1.0
        assert (
            abs(result["initGross"][0] - expected_gross) < 0.01
        ), f"Expected initGross[0] ~ {expected_gross}, got {result['initGross'][0]}"

        # Now with acEfficiency=95.0 (lower), RTE should be reduced further
        params2 = {**params, "acEfficiency": 95.0}
        result2 = calculate_energy_accounting(params2, soh, rte, dod, aug_qty, efficiency_factors=None)
        # cycle_rte = 0.85 * 0.95 = 0.8075
        expected_gross2 = 5 * 10 * 0.9 * 0.8075 * 1.0
        assert (
            abs(result2["initGross"][0] - expected_gross2) < 0.01
        ), f"Expected initGross[0] ~ {expected_gross2}, got {result2['initGross'][0]}"
        assert result2["initGross"][0] < result["initGross"][0], "Lower acEfficiency should produce lower initGross"

    def test_simulation_engine_null_factors_via_api(self, client, auth_headers_eng):
        """POST /api/simulation/run with survey_params containing
        efficiencyFactors=None and degradation containing custom rte array.
        Verify the response rte matches custom values."""
        design_output = {
            "container": {"ratedEnergyMwh": 5},
            "pcs": {"ratedPowerMW": 2.5},
            "containerQty": 10,
            "pcsQty": 10,
            "duration": 2,
        }

        custom_rte = [88.0] * 26
        custom_soh = [98.0] * 26

        resp = _post(
            client,
            "/api/simulation/run",
            {
                "design_output": design_output,
                "survey_params": {**SURVEY_PARAMS, "efficiencyFactors": None},
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

        # efficiencyCurves should be None when efficiencyFactors is None
        assert data.get("efficiencyCurves") is None, "efficiencyCurves should be None via API with null factors"

        # rte should match custom values
        result_rte = data.get("rte", [])
        assert len(result_rte) == 26, f"Expected 26 rte values, got {len(result_rte)}"
        for i in range(26):
            assert (
                abs(result_rte[i] - custom_rte[i]) < 0.01
            ), f"Year {i}: rte should be {custom_rte[i]}, got {result_rte[i]}"

    def test_missing_key_vs_explicit_none(self):
        """Verify that when 'efficiencyFactors' key is ABSENT from system_params,
        it behaves like FACTOR_DEFAULTS. When explicitly None, it uses custom RTE.
        This tests the pipeline.py fix at lines 239-241."""
        from services.pipeline import NUM_YEARS, calculate_full_pipeline

        # Common degradation data
        degradation = {
            "soh": [95.0] * NUM_YEARS,
            "rte": [90.0] * NUM_YEARS,
            "dod": [90.0] * NUM_YEARS,
            "augQty": [0] * NUM_YEARS,
        }

        # Case 1: Key ABSENT — should behave like FACTOR_DEFAULTS
        params_absent = {
            "ratedEnergy": 5,
            "initContainerQty": 10,
            "initPcsQty": 10,
            "duration": 2,
            "cyclesPerDay": 1,
            "temperature": 25,
            "dod": 90,
            "cRate": 0.5,
            "acEfficiency": 100.0,
            "requiredEnergy": 200,
            # "efficiencyFactors" NOT present
        }

        result_absent = calculate_full_pipeline(params_absent, degradation=degradation)
        assert (
            result_absent["efficiencyCurves"] is not None
        ), "When key is absent, efficiencyCurves should be computed (default factors)"

        # Case 2: Explicitly None — should use custom RTE
        params_none = {**params_absent, "efficiencyFactors": None}

        result_none = calculate_full_pipeline(params_none, degradation=degradation)
        assert (
            result_none["efficiencyCurves"] is None
        ), "When key is explicitly None, efficiencyCurves should be None (custom RTE)"

        # The results should differ
        assert (
            result_absent["initGross"][0] != result_none["initGross"][0]
        ), "Absent key vs explicit None should produce different initGross"

        # Case 3: Explicitly FACTOR_DEFAULTS — should match absent case
        from services.pipeline import FACTOR_DEFAULTS

        params_defaults = {**params_absent, "efficiencyFactors": FACTOR_DEFAULTS}

        result_defaults = calculate_full_pipeline(params_defaults, degradation=degradation)
        assert (
            result_absent["initGross"][0] == result_defaults["initGross"][0]
        ), "Absent key should produce same result as explicit FACTOR_DEFAULTS"
