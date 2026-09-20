import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from app.main import app

@pytest.mark.asyncio
async def test_market_prices_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/market")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        item = data[0]
        assert "crop" in item
        assert "currentPrice" in item
        assert "trend" in item
        assert "nearbyMarkets" in item
        assert "priceHistory" in item

@pytest.mark.asyncio
async def test_market_history_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/market/history?crop=Cotton&days=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "day" in data[0]
            assert "price" in data[0]

@pytest.mark.asyncio
async def test_market_nearby_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/market/nearby?crop=Cotton&ref_mandi=Rajkot%20APMC")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "name" in data[0]
            assert "price" in data[0]

@pytest.mark.asyncio
async def test_market_trends_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/market/trends?crop=Cotton")
        assert response.status_code == 200
        data = response.json()
        assert "crop" in data
        assert "currentPrice" in data
        assert "trend" in data
        assert "change7d" in data

@pytest.mark.asyncio
async def test_market_provider_failure_fallback():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with patch("app.integrations.market_provider.MockMarketProvider.get_current_prices", side_effect=Exception("Connection timeout")):
            with patch("app.integrations.redis_cache.CacheService.get_json", return_value=None):
                response = await client.get("/api/market")
                assert response.status_code == 200
                data = response.json()
                assert len(data) > 0
