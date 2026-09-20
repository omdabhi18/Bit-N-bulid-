from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any, Optional

from app.integrations.storage_provider import storage_service

router = APIRouter(prefix="/storage", tags=["Cloud Storage (Cloudinary / S3)"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form("documents")
) -> Dict[str, Any]:
    """Securely upload file to Cloudinary / S3 / Local storage with validation."""
    file_bytes = await file.read()
    content_type = file.content_type or "image/jpeg"
    return await storage_service.upload_file(
        file_bytes=file_bytes,
        filename=file.filename or "upload.jpg",
        content_type=content_type,
        folder=folder
    )

@router.delete("/{public_id:path}")
async def delete_file(public_id: str):
    """Delete file from cloud storage."""
    success = await storage_service.delete_file(public_id)
    if not success:
        raise HTTPException(status_code=404, detail="File could not be deleted or was not found.")
    return {"status": "success", "message": f"File {public_id} deleted successfully."}

@router.get("/url/{public_id:path}")
async def get_file_url(public_id: str):
    """Get public accessible URL for the stored file."""
    url = await storage_service.get_file_url(public_id)
    return {"public_id": public_id, "url": url}

@router.get("/signed-url/{public_id:path}")
async def get_signed_url(public_id: str, expires_in: int = 3600):
    """Generate time-limited signed URL for secure download."""
    signed_url = await storage_service.generate_signed_url(public_id, expires_in=expires_in)
    return {"public_id": public_id, "signed_url": signed_url, "expires_in": expires_in}
