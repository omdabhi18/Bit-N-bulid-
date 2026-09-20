import pytest

@pytest.mark.asyncio
async def test_weather_forecast_endpoint(client):
    response = await client.get("/api/weather/forecast")
    assert response.status_code == 200
    data = response.json()
    assert "current" in data
    assert "hourly" in data
    assert "daily" in data
    assert data["current"]["temp"] > 0
    assert len(data["hourly"]) >= 3
    assert len(data["daily"]) >= 7

@pytest.mark.asyncio
async def test_weather_current_endpoint(client):
    response = await client.get("/api/weather/current")
    assert response.status_code == 200
    data = response.json()
    assert "temp" in data
    assert "humidity" in data
    assert "rainfallProb" in data

@pytest.mark.asyncio
async def test_weather_hourly_endpoint(client):
    response = await client.get("/api/weather/hourly")
    assert response.status_code == 200
    hourly = response.json()
    assert isinstance(hourly, list)
    assert len(hourly) > 0
    assert "rainProb" in hourly[0]

@pytest.mark.asyncio
async def test_weather_window_irrigation_decision(client):
    response = await client.get("/api/weather/window")
    assert response.status_code == 200
    data = response.json()
    assert "shouldIrrigateNow" in data
    assert "confidence" in data
    assert "factors" in data
    assert "bestWindow" in data
    assert data["confidence"] >= 80
