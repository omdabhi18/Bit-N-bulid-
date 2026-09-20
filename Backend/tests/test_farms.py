import pytest

@pytest.mark.asyncio
async def test_get_farm_profile(client):
    response = await client.get("/api/farms/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["farmName"] == "GreenValley Smart Farms"
    assert data["farmerName"] == "Kishanbhai Patel"
    assert data["district"] == "Rajkot"
    assert len(data["crops"]) >= 3

@pytest.mark.asyncio
async def test_get_fields(client):
    response = await client.get("/api/farms/fields")
    assert response.status_code == 200
    fields = response.json()
    assert len(fields) == 3
    field_a = next(f for f in fields if f["id"] == "field-a")
    assert field_a["name"] == "Field A - South Valley"
    assert field_a["crop"] == "BT Cotton (કપાસ)"
    assert field_a["soilMoisture"] == 31.0
    assert len(field_a["coordinates"]) == 4

@pytest.mark.asyncio
async def test_get_crops(client):
    response = await client.get("/api/crops")
    assert response.status_code == 200
    data = response.json()
    crops = data.get("crops", data)
    assert len(crops) >= 3
