import pytest

@pytest.mark.asyncio
async def test_get_action_plans(client):
    response = await client.get("/api/action-plans")
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) >= 2
    plan = next(p for p in plans if p["id"] == "PLAN-1024")
    assert plan["estimatedCost"] == 45.0
    assert plan["constraints"]["costBudget"] is not None

@pytest.mark.asyncio
async def test_approve_plan(client):
    response = await client.post("/api/action-plans/PLAN-1024/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
