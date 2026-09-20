import pytest

@pytest.mark.asyncio
async def test_get_risks(client):
    response = await client.get("/api/risks")
    assert response.status_code == 200
    risks = response.json()
    assert len(risks) >= 4
    water_risk = next(r for r in risks if "Water Stress" in r["category"])
    assert water_risk["severity"] == "High"
    assert water_risk["field"] == "Field A (Cotton)"

@pytest.mark.asyncio
async def test_generate_plan_from_risk(client):
    response = await client.post("/api/risks/risk-03/generate-plan")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "PLAN-" in data["planId"]
