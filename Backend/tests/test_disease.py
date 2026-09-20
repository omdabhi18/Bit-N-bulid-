import pytest

@pytest.mark.asyncio
async def test_disease_catalog(client):
    res = await client.get("/api/disease/catalog")
    assert res.status_code == 200
    catalog = res.json()
    assert len(catalog) == 4
    assert catalog[0]["crop"] == "Cotton (કપાસ)"

@pytest.mark.asyncio
async def test_analyze_sample(client):
    res = await client.post("/api/disease/analyze", data={"sampleId": "dis-01"})
    assert res.status_code == 200
    data = res.json()
    assert data["confidence"] == 88
    assert "remedy" in str(data["recommendedRemedy"]).lower() or "organic" in data["recommendedRemedy"]

@pytest.mark.asyncio
async def test_escalation_flow(client):
    # Create escalation
    res = await client.post("/api/disease/escalate", json={
        "field": "Field B (Wheat)",
        "crop": "Wheat",
        "issue": "Unusual leaf necrosis",
        "aiConfidence": 55,
        "reason": "Low vision confidence",
        "telemetrySnapshot": {"moisture": "40%"}
    })
    assert res.status_code == 200
    assert "ESC-" in res.json()["id"]
