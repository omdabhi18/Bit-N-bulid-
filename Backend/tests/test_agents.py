import pytest

@pytest.mark.asyncio
async def test_get_agents(client):
    res = await client.get("/api/agents")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) == 8
    assert any(a["id"] == "orchestrator" for a in agents)
    assert any(a["id"] == "soil" for a in agents)
    assert any(a["id"] == "weather" for a in agents)

@pytest.mark.asyncio
async def test_trigger_orchestration_cycle(client):
    res = await client.post("/api/agents/orchestrate", json={"farmId": "farm-greenvalley-01"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["agentsRan"]) >= 10
    assert data["detectedRisksCount"] >= 1
