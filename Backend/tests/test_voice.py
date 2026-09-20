import pytest

@pytest.mark.asyncio
async def test_kisan_voice_gujarati(client):
    res = await client.post("/api/voice/query", json={
        "query": "મારા કપાસમાં આજે પાણી આપવું જોઈએ?",
        "language": "gu"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["actionRecommendation"] == "irrigate"
    assert "૩૧%" in data["replyText"] or "પાણી" in data["replyText"] or "ડ્રિપ" in data["replyText"]

@pytest.mark.asyncio
async def test_kisan_voice_english(client):
    res = await client.post("/api/voice/query", json={
        "query": "Should I irrigate Field A today?",
        "language": "en"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["actionRecommendation"] == "irrigate"
    assert "Field A" in data["replyText"]
