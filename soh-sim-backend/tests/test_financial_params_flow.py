"""
SOH-SIM Financial Params Flow 测试

验证完整的财务参数流：从 API 通过 FinancialEngine 到 calculator.py。
测试 CAPEX 是否正确计算，所有财务指标是否有效。
"""

import json
import os
import uuid

import pytest

# 必须在导入 app 前设置
os.environ.setdefault("TEST_DATABASE_URI", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-financial-params-2026")
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


# ==================== Simulation Fixture ====================


@pytest.fixture()
def simulation_output():
    """Standard simulation output for financial input."""
    base = 240.0
    total_ac = [max(0, base * (1 - 0.005 * i)) for i in range(26)]
    return {
        "totalAcUsable": total_ac,
        "soh": [100 * (1 - 0.005 * i) for i in range(26)],
        "rte": [97 * (1 - 0.002 * i) for i in range(26)],
        "meetsReq": [v >= 200 for v in total_ac],
    }


# ==================== Test Class ====================


class TestFinancialParamsFlow:
    """Verify the complete financial parameter flow from API through
    FinancialEngine to calculator.py."""

    def test_capex_computed_from_design(self, client, auth_headers_eng, simulation_output):
        """POST /api/financial/calculate with design_output containing
        container={ratedEnergyMwh:5}, containerQty=100.
        Verify capexBreakdown.equipment is approximately 100,000,000
        (500MWh * $200,000/MWh), NOT the old default of 20,000,000."""
        resp = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": {
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 100,
                    "pcsQty": 100,
                    "duration": 2,
                },
                "survey_params": {"location": "china", "ratedEnergy": 100, "totalPower": 50},
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        capex = data.get("capexBreakdown", {})
        equipment = capex.get("equipment", 0)

        # totalEnergyMwh = 5 * 100 = 500 MWh
        # equipment = 500 * 200000 = 100,000,000
        expected_equipment = 100_000_000
        assert (
            abs(equipment - expected_equipment) < 1_000
        ), f"Expected equipment ~ {expected_equipment}, got {equipment}"

        # NOT the old default of 20,000,000
        assert equipment > 50_000_000, f"Equipment {equipment} should be much larger than old default 20M"

    def test_capex_from_explicit_totalEnergyMwh(self, client, auth_headers_eng, simulation_output):
        """POST with design_output containing totalEnergyMwh=200.
        Verify capexBreakdown.equipment is approximately 40,000,000."""
        resp = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": {
                    "totalEnergyMwh": 200,
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 10,
                    "pcsQty": 10,
                    "duration": 2,
                },
                "survey_params": {"location": "china", "ratedEnergy": 100, "totalPower": 50},
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        capex = data.get("capexBreakdown", {})
        equipment = capex.get("equipment", 0)

        # totalEnergyMwh=200 * $200,000/MWh = 40,000,000
        expected_equipment = 40_000_000
        assert (
            abs(equipment - expected_equipment) < 1_000
        ), f"Expected equipment ~ {expected_equipment}, got {equipment}"

    def test_revenue_model_china(self, client, auth_headers_eng, simulation_output):
        """POST with survey_params.location='china'. Verify revenueModel has
        arbitrage.enabled=true, ancillary.enabled=false."""
        resp = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": {
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 10,
                    "pcsQty": 10,
                    "duration": 2,
                },
                "survey_params": {"location": "china", "ratedEnergy": 100, "totalPower": 50},
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        revenue = data.get("revenueModel", {})
        assert revenue.get("arbitrage", {}).get("enabled") is True, "China: arbitrage should be enabled"
        assert revenue.get("ancillary", {}).get("enabled") is False, "China: ancillary should be disabled"
        assert revenue.get("capacity", {}).get("enabled") is True, "China: capacity should be enabled"

    def test_revenue_model_cambodia_default(self, client, auth_headers_eng, simulation_output):
        """POST with survey_params.location='cambodia' (no specific match).
        Verify revenueModel has all streams enabled (default)."""
        resp = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": {
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 10,
                    "pcsQty": 10,
                    "duration": 2,
                },
                "survey_params": {"location": "cambodia", "ratedEnergy": 100, "totalPower": 50},
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        revenue = data.get("revenueModel", {})
        # Default model has all streams enabled
        assert revenue.get("arbitrage", {}).get("enabled") is True, "Default: arbitrage should be enabled"
        assert revenue.get("capacity", {}).get("enabled") is True, "Default: capacity should be enabled"
        assert revenue.get("ancillary", {}).get("enabled") is True, "Default: ancillary should be enabled"

    def test_financial_metrics_valid(self, client, auth_headers_eng, simulation_output):
        """POST with valid simulation_output (26-element totalAcUsable).
        Verify projectIrr is between 0 and 100, npv is a number, lcos is positive."""
        resp = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": {
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 10,
                    "pcsQty": 10,
                    "duration": 2,
                },
                "survey_params": {"location": "china", "ratedEnergy": 100, "totalPower": 50},
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        metrics = data.get("metrics", {})
        assert "projectIrr" in metrics, "Missing projectIrr"
        assert "npv" in metrics, "Missing npv"
        assert "lcos" in metrics, "Missing lcos"

        irr = metrics["projectIrr"]
        npv = metrics["npv"]
        lcos = metrics["lcos"]

        assert isinstance(irr, (int, float)), f"IRR should be numeric, got {type(irr)}"
        assert isinstance(npv, (int, float)), f"NPV should be numeric, got {type(npv)}"
        assert isinstance(lcos, (int, float)), f"LCOS should be numeric, got {type(lcos)}"

        # IRR should be reasonable (0-100%)
        assert 0 <= irr <= 100, f"IRR {irr} should be between 0 and 100"

        # LCOS should be positive
        assert lcos > 0, f"LCOS {lcos} should be positive"

        # NPV can be positive or negative but should be finite
        import math

        assert math.isfinite(npv), f"NPV {npv} should be finite"

    def test_sensitivity_analysis(self, client, auth_headers_eng, simulation_output):
        """POST /api/financial/sensitivity with total_ac_usable array.
        Verify returns 4 scenarios (capex_plus_15, capex_minus_15,
        price_plus_20, price_minus_20)."""
        resp = _post(
            client,
            "/api/financial/sensitivity",
            {
                "total_ac_usable": simulation_output["totalAcUsable"],
                "financial_params": {},
            },
            auth_headers_eng,
        )
        data = _assert_success(resp)

        # Should contain exactly 4 scenarios
        expected_scenarios = ["capex_plus_15", "capex_minus_15", "price_plus_20", "price_minus_20"]
        for scenario in expected_scenarios:
            assert scenario in data, f"Missing sensitivity scenario: {scenario}"
            scenario_data = data[scenario]
            if scenario_data is not None:
                assert "irr" in scenario_data, f"{scenario} missing irr"
                assert "npv" in scenario_data, f"{scenario} missing npv"
                assert "lcos" in scenario_data, f"{scenario} missing lcos"

        # CAPEX+15 should have lower IRR than CAPEX-15
        if data.get("capex_plus_15") and data.get("capex_minus_15"):
            irr_plus = data["capex_plus_15"].get("irr")
            irr_minus = data["capex_minus_15"].get("irr")
            if irr_plus is not None and irr_minus is not None:
                assert (
                    irr_plus <= irr_minus
                ), f"Higher CAPEX ({irr_plus}) should not have higher IRR than lower CAPEX ({irr_minus})"

    def test_discount_rate_affects_npv(self, client, auth_headers_eng, simulation_output):
        """Run financial calculate twice with different discountRate values.
        Verify higher discount rate produces lower npv."""
        design_output = {
            "container": {"ratedEnergyMwh": 5},
            "pcs": {"ratedPowerMW": 2.5},
            "containerQty": 10,
            "pcsQty": 10,
            "duration": 2,
        }
        survey_params = {"location": "china", "ratedEnergy": 100, "totalPower": 50}

        # Low discount rate
        resp_low = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": design_output,
                "survey_params": survey_params,
                "financial_params": {"discountRate": 5.0},
            },
            auth_headers_eng,
        )
        data_low = _assert_success(resp_low)
        npv_low = data_low["metrics"]["npv"]

        # High discount rate
        resp_high = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": simulation_output,
                "design_output": design_output,
                "survey_params": survey_params,
                "financial_params": {"discountRate": 12.0},
            },
            auth_headers_eng,
        )
        data_high = _assert_success(resp_high)
        npv_high = data_high["metrics"]["npv"]

        # Higher discount rate should produce lower NPV
        assert (
            npv_high < npv_low
        ), f"Higher discount rate NPV ({npv_high}) should be less than lower discount rate NPV ({npv_low})"

    def test_full_financial_chain(self, client, auth_headers_eng):
        """POST /api/simulation/run -> extract totalAcUsable ->
        POST /api/financial/calculate with that data.
        Verify the chain works end-to-end and produces valid metrics."""
        # Step 1: Run simulation
        sim_resp = _post(
            client,
            "/api/simulation/run",
            {
                "design_output": {
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 10,
                    "pcsQty": 10,
                    "duration": 2,
                },
                "survey_params": SURVEY_PARAMS,
            },
            auth_headers_eng,
        )
        sim_data = _assert_success(sim_resp)

        # Verify simulation produced usable data
        total_ac = sim_data["totalAcUsable"]
        assert len(total_ac) == 26, "Simulation should produce 26-year data"
        assert total_ac[0] > 0, "Year 0 totalAcUsable should be positive"

        # Step 2: Run financial with simulation output
        fin_resp = _post(
            client,
            "/api/financial/calculate",
            {
                "simulation_output": {
                    "totalAcUsable": total_ac,
                    "soh": sim_data.get("soh", [100] * 26),
                    "rte": sim_data.get("rte", [97] * 26),
                    "meetsReq": sim_data.get("meetsReq", [True] * 26),
                },
                "design_output": {
                    "container": {"ratedEnergyMwh": 5},
                    "pcs": {"ratedPowerMW": 2.5},
                    "containerQty": 10,
                    "pcsQty": 10,
                    "duration": 2,
                },
                "survey_params": {"location": "china", "ratedEnergy": 100, "totalPower": 50},
            },
            auth_headers_eng,
        )
        fin_data = _assert_success(fin_resp)

        # Verify financial metrics are valid
        metrics = fin_data.get("metrics", {})
        assert "projectIrr" in metrics, "Missing projectIrr in chain result"
        assert "npv" in metrics, "Missing npv in chain result"
        assert "lcos" in metrics, "Missing lcos in chain result"
        assert metrics["lcos"] > 0, "LCOS should be positive"

        # Verify cashflow table exists
        cashflow = fin_data.get("cashflowTable", [])
        assert len(cashflow) > 0, "Cashflow table should not be empty"
