import io
import pytest
from PIL import Image
from httpx import AsyncClient, ASGITransport
from app.main import app

def create_test_image(width=200, height=200, fmt="JPEG") -> bytes:
    img = Image.new("RGB", (width, height), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

@pytest.mark.asyncio
async def test_storage_upload_valid_image():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        img_bytes = create_test_image()
        files = {"file": ("test_crop.jpg", img_bytes, "image/jpeg")}
        response = await client.post("/api/storage/upload", files=files, data={"folder": "test_crops"})
        assert response.status_code == 200
        data = response.json()
        assert "url" in data
        assert "public_id" in data
        assert "storage_provider" in data
        assert "metadata" in data

@pytest.mark.asyncio
async def test_storage_upload_invalid_mime_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        files = {"file": ("malicious.txt", b"plain text script", "text/plain")}
        response = await client.post("/api/storage/upload", files=files)
        assert response.status_code == 400
        data = response.json()
        err_msg = data.get("detail") or data.get("error", {}).get("message", "")
        assert "Invalid image format" in err_msg

@pytest.mark.asyncio
async def test_storage_upload_too_small_dimensions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        tiny_bytes = create_test_image(width=10, height=10)
        files = {"file": ("tiny.jpg", tiny_bytes, "image/jpeg")}
        response = await client.post("/api/storage/upload", files=files)
        assert response.status_code == 400
        data = response.json()
        err_msg = data.get("detail") or data.get("error", {}).get("message", "")
        assert "dimensions too small" in err_msg

@pytest.mark.asyncio
async def test_disease_analyze_with_file_upload():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        img_bytes = create_test_image(width=300, height=300)
        files = {"file": ("field_leaf.jpg", img_bytes, "image/jpeg")}
        data = {"cropId": "cotton"}
        response = await client.post("/api/disease/analyze", files=files, data=data)
        assert response.status_code == 200
        res = response.json()
        assert res["supported"] is True
        assert "diseaseName" in res
        assert "confidence" in res
        assert "imageUrl" in res
