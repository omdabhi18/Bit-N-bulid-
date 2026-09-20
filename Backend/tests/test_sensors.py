import pytest

@pytest.mark.asyncio
async def test_monitoring_telemetry(client):
    response = await client.get("/api/monitoring/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert "telemetry" in data
    assert "timeSeries" in data
    assert "npkRadar" in data
    assert "sensors" in data
    assert len(data["sensors"]) == 4

@pytest.mark.asyncio
async def test_trigger_valve(client):
    response = await client.post("/api/sensors/valve/trigger", json={
        "fieldId": "field-a",
        "minutes": 35
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "Running"
    assert data["minutes"] == 35
