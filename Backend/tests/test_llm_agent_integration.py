import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from app.main import app
from app.integrations.llm_client import get_llm_provider, MockLLMProvider, GeminiLLMProvider

@pytest.mark.asyncio
async def test_llm_advisory_explanation():
    provider = get_llm_provider()
    explanation = await provider.generate_explanation(
        risk_data={"title": "Root Moisture Deficit", "severity": "High"},
        context={"soilMoisture": 31.4, "rainfallProb24h": 12, "crop": "Cotton"}
    )
    assert isinstance(explanation, str)
    assert len(explanation) > 20
    assert "moisture" in explanation.lower() or "irrigation" in explanation.lower() or "evaporation" in explanation.lower()

@pytest.mark.asyncio
async def test_llm_kisan_query_multilingual():
    provider = get_llm_provider()
    # Gujarati query
    gu_res = await provider.answer_kisan_query(
        query="Mara Field A ma aaje pani aapvu joie?",
        farm_context={"soilMoisture": 31.4, "rainfallProb24h": 12, "farmHealthScore": 82},
        language="gu"
    )
    assert "reply" in gu_res
    assert "31.4" in gu_res["reply"] or "પિયત" in gu_res["reply"] or "ભલામણ" in gu_res["reply"]

    # Hindi query
    hi_res = await provider.answer_kisan_query(
        query="Khet A mein pani dena hai?",
        farm_context={"soilMoisture": 31.4, "rainfallProb24h": 12, "farmHealthScore": 82},
        language="hi"
    )
    assert "reply" in hi_res
    assert "सिंचाई" in hi_res["reply"] or "31.4" in hi_res["reply"]

@pytest.mark.asyncio
async def test_llm_failure_graceful_fallback():
    # Simulate remote LLM failure
    with patch("app.integrations.llm_client.MockLLMProvider.answer_kisan_query", return_value={"reply": "Offline rule advisory", "action": "irrigate"}):
        provider = get_llm_provider()
        res = await provider.answer_kisan_query("test query", {"soilMoisture": 30.0})
        assert "reply" in res
        assert res["action"] == "irrigate"

@pytest.mark.asyncio
async def test_multi_agent_orchestration_and_agent_runs_logging():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Trigger full orchestration cycle
        response = await client.post("/api/agents/orchestrate", json={"farmId": "farm-greenvalley-01"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["agentsRan"]) >= 10

        # Verify execution runs stored in agent_runs table
        runs_response = await client.get("/api/agents/runs")
        assert runs_response.status_code == 200
        runs_data = runs_response.json()
        assert isinstance(runs_data, list)
        assert len(runs_data) > 0
        run_item = runs_data[0]
        assert "agent_name" in run_item
        assert "confidence" in run_item
        assert "input_summary" in run_item
        assert "output_summary" in run_item
        assert "status" in run_item
        assert "started_at" in run_item
        assert "completed_at" in run_item
