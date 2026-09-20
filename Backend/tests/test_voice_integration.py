import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from app.main import app

@pytest.mark.asyncio
async def test_voice_query_gujarati_with_farm_context():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        req = {
            "query": "Mara Field A ma aaje pani aapvu joie?",
            "language": "gu"
        }
        response = await client.post("/api/voice/query", json=req)
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "gu"
        assert "replyText" in data
        assert len(data["replyText"]) > 10
        # Verify farm context factors are returned
        assert len(data["telemetryFactorsUsed"]) > 0
        assert data["actionRecommendation"] in ["irrigate", "none", "advisory", "fertilize", "sell"]

@pytest.mark.asyncio
async def test_voice_query_hindi():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        req = {
            "query": "Khet A mein aaj paani dena hai?",
            "language": "hi"
        }
        response = await client.post("/api/voice/query", json=req)
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "hi"
        assert "replyText" in data

@pytest.mark.asyncio
async def test_voice_query_english():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        req = {
            "query": "Should I irrigate Field A today?",
            "language": "en"
        }
        response = await client.post("/api/voice/query", json=req)
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
        assert "Cotton" in data["replyText"] or "moisture" in data["replyText"].lower()

@pytest.mark.asyncio
async def test_voice_transcribe():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        files = {"file": ("farmer_audio.wav", b"dummy_audio_bytes_16khz", "audio/wav")}
        response = await client.post("/api/voice/transcribe", files=files, data={"language": "gu"})
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert data["language"] == "gu"

@pytest.mark.asyncio
async def test_voice_synthesize():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        data = {"text": "નમસ્તે ખેડૂત મિત્ર", "language": "gu"}
        response = await client.post("/api/voice/synthesize", data=data)
        assert response.status_code == 200
        res = response.json()
        assert "mime_type" in res

@pytest.mark.asyncio
async def test_voice_tts_failure_fallback():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with patch("app.integrations.text_to_speech.GTTSVoiceProvider.synthesize", side_effect=Exception("TTS server offline")):
            req = {"query": "Pani aapvu?", "language": "gu"}
            response = await client.post("/api/voice/query", json=req)
            assert response.status_code == 200
            data = response.json()
            assert "replyText" in data
            assert data["audioUrl"] is None
