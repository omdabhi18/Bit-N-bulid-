import pytest
from app.models.crop import Crop
from app.models.disease import DiseaseAnalysis
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_get_crops_catalog(client):
    response = await client.get("/api/crops")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["crops"]) >= 24

@pytest.mark.asyncio
async def test_search_crops_english_and_gujarati(client):
    # English search
    res_en = await client.get("/api/crops?search=Cotton")
    assert res_en.status_code == 200
    crops_en = res_en.json()["crops"]
    assert any(c["id"] == "cotton" for c in crops_en)

    # Gujarati search
    res_gu = await client.get("/api/crops?search=કપાસ")
    assert res_gu.status_code == 200
    crops_gu = res_gu.json()["crops"]
    assert any(c["id"] == "cotton" for c in crops_gu)

@pytest.mark.asyncio
async def test_filter_crops_by_capability(client):
    res_supported = await client.get("/api/crops?disease_ai_supported=true")
    assert res_supported.status_code == 200
    crops_supported = res_supported.json()["crops"]
    assert all(c["disease_ai_supported"] is True for c in crops_supported)
    assert len(crops_supported) == 12

    res_unsupported = await client.get("/api/crops?disease_ai_supported=false")
    assert res_unsupported.status_code == 200
    crops_unsupported = res_unsupported.json()["crops"]
    assert all(c["disease_ai_supported"] is False for c in crops_unsupported)
    assert len(crops_unsupported) == 12

@pytest.mark.asyncio
async def test_analyze_supported_crop(client, db_session):
    response = await client.post(
        "/api/disease/analyze",
        data={"cropId": "cotton"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["supported"] is True
    assert data["requiresExpertEscalation"] is False
    assert "Bacterial Blight" in data["diseaseName"]
    assert data["crop_id"] == "cotton"

    # Verify persistence in database
    res = await db_session.execute(
        select(DiseaseAnalysis).where(DiseaseAnalysis.id == data["id"])
    )
    analysis = res.scalars().first()
    assert analysis is not None
    assert analysis.crop_id == "cotton"

@pytest.mark.asyncio
async def test_analyze_unsupported_crop(client):
    response = await client.post(
        "/api/disease/analyze",
        data={"cropId": "bajra"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["supported"] is False
    assert data["requiresExpertEscalation"] is True
    assert "AI analysis is currently unavailable for this crop" in data["message"]
    assert data["confidence"] == 0

@pytest.mark.asyncio
async def test_analyze_demo_sample(client):
    response = await client.post(
        "/api/disease/analyze",
        data={"sampleId": "dis-02"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["supported"] is True
    assert "Wheat" in data["crop"]
    assert "Yellow / Stripe Rust" in data["diseaseName"]
