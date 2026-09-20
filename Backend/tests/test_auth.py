import pytest

@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post("/api/auth/login", json={
        "email": "kishanbhai@greenvalley.in",
        "password": "Password123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "kishanbhai@greenvalley.in"

@pytest.mark.asyncio
async def test_login_failure(client):
    response = await client.post("/api/auth/login", json={
        "email": "kishanbhai@greenvalley.in",
        "password": "WrongPassword"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_dashboard_endpoint(client):
    response = await client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "farmHealthScore" in data
    assert "soilMoisture" in data
    assert len(data["fields"]) >= 3
    assert data["primaryAdvisory"] is not None
