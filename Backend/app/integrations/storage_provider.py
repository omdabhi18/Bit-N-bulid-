import os
import io
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from PIL import Image
from fastapi import HTTPException

from app.config import settings
from app.utils.logger import logger

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MIN_DIMENSION = 50
MAX_DIMENSION = 8000

def validate_image_file(file_bytes: bytes, content_type: str) -> Dict[str, Any]:
    """Validate MIME type, size, and image dimensions before upload."""
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format '{content_type}'. Allowed: JPEG, PNG, WEBP."
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Image size exceeds 10MB limit (received {len(file_bytes) / (1024*1024):.2f}MB)."
        )

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.verify()
        width, height = image.size
        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            raise HTTPException(
                status_code=400,
                detail=f"Image dimensions too small ({width}x{height}). Minimum required: {MIN_DIMENSION}x{MIN_DIMENSION}px."
            )
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            raise HTTPException(
                status_code=400,
                detail=f"Image dimensions too large ({width}x{height}). Maximum allowed: {MAX_DIMENSION}x{MAX_DIMENSION}px."
            )
        return {
            "format": image.format,
            "width": width,
            "height": height,
            "size_bytes": len(file_bytes),
            "mime_type": content_type
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Corrupt or unreadable image file: {str(e)}"
        )


class StorageProvider(ABC):
    """Abstract Base Class for file and image storage providers."""

    @abstractmethod
    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "crops"
    ) -> Dict[str, Any]:
        """Upload file and return dict with url, public_id, provider, metadata."""
        pass

    @abstractmethod
    async def delete_file(self, public_id: str) -> bool:
        """Delete file from storage by its public_id or object key."""
        pass

    @abstractmethod
    async def get_file_url(self, public_id: str) -> str:
        """Get accessible URL for the file."""
        pass

    @abstractmethod
    async def generate_signed_url(self, public_id: str, expires_in: int = 3600) -> str:
        """Generate a time-limited signed URL for secure access."""
        pass


class CloudinaryStorageProvider(StorageProvider):
    """Cloudinary Cloud Storage Provider for high-performance image management."""

    def __init__(self):
        self.cloud_name = settings.CLOUDINARY_CLOUD_NAME
        self.api_key = settings.CLOUDINARY_API_KEY
        self.api_secret = settings.CLOUDINARY_API_SECRET
        self._configured = bool(
            self.cloud_name
            and self.api_key
            and self.api_secret
            and self.api_secret != "your_cloudinary_api_secret"
        )
        if self._configured:
            import cloudinary
            cloudinary.config(
                cloud_name=self.cloud_name,
                api_key=self.api_key,
                api_secret=self.api_secret,
                secure=True
            )
            logger.info("Cloudinary storage provider initialized successfully.")
        else:
            logger.info("Cloudinary credentials not configured. Local fallback will be used.")

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "krishinetra/crops"
    ) -> Dict[str, Any]:
        meta = validate_image_file(file_bytes, content_type)
        if not self._configured:
            return await LocalStorageProvider().upload_file(file_bytes, filename, content_type, folder)

        import cloudinary.uploader
        try:
            response = cloudinary.uploader.upload(
                file_bytes,
                folder=folder,
                resource_type="image"
            )
            return {
                "url": response.get("secure_url"),
                "public_id": response.get("public_id"),
                "storage_provider": "cloudinary",
                "metadata": {
                    **meta,
                    "format": response.get("format"),
                    "bytes": response.get("bytes"),
                    "created_at": response.get("created_at")
                }
            }
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {e}. Falling back to local storage.")
            return await LocalStorageProvider().upload_file(file_bytes, filename, content_type, folder)

    async def delete_file(self, public_id: str) -> bool:
        if not self._configured:
            return await LocalStorageProvider().delete_file(public_id)

        import cloudinary.uploader
        try:
            res = cloudinary.uploader.destroy(public_id)
            return res.get("result") == "ok"
        except Exception as e:
            logger.error(f"Cloudinary delete failed for {public_id}: {e}")
            return False

    async def get_file_url(self, public_id: str) -> str:
        if not self._configured:
            return await LocalStorageProvider().get_file_url(public_id)
        import cloudinary.utils
        return cloudinary.utils.cloudinary_url(public_id, secure=True)[0]

    async def generate_signed_url(self, public_id: str, expires_in: int = 3600) -> str:
        # Cloudinary URLs are secure by default
        return await self.get_file_url(public_id)


class S3StorageProvider(StorageProvider):
    """AWS S3 / S3-compatible object storage provider."""

    def __init__(self):
        self.bucket = settings.AWS_BUCKET_NAME
        self.region = settings.AWS_REGION
        self.access_key = settings.AWS_ACCESS_KEY_ID
        self.secret_key = settings.AWS_SECRET_ACCESS_KEY
        self._configured = bool(self.bucket and self.access_key and self.secret_key)

    def _get_client(self):
        import boto3
        return boto3.client(
            "s3",
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "crops"
    ) -> Dict[str, Any]:
        meta = validate_image_file(file_bytes, content_type)
        if not self._configured:
            return await LocalStorageProvider().upload_file(file_bytes, filename, content_type, folder)

        key = f"{folder}/{uuid.uuid4().hex[:12]}_{filename}"
        try:
            client = self._get_client()
            client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
            return {
                "url": url,
                "public_id": key,
                "storage_provider": "s3",
                "metadata": meta
            }
        except Exception as e:
            logger.error(f"S3 upload failed: {e}. Falling back to local storage.")
            return await LocalStorageProvider().upload_file(file_bytes, filename, content_type, folder)

    async def delete_file(self, public_id: str) -> bool:
        if not self._configured:
            return await LocalStorageProvider().delete_file(public_id)
        try:
            client = self._get_client()
            client.delete_object(Bucket=self.bucket, Key=public_id)
            return True
        except Exception as e:
            logger.error(f"S3 delete failed: {e}")
            return False

    async def get_file_url(self, public_id: str) -> str:
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{public_id}"

    async def generate_signed_url(self, public_id: str, expires_in: int = 3600) -> str:
        if not self._configured:
            return await LocalStorageProvider().generate_signed_url(public_id, expires_in)
        client = self._get_client()
        return client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": public_id},
            ExpiresIn=expires_in
        )


class LocalStorageProvider(StorageProvider):
    """Local disk storage provider for development, tests, and offline execution."""

    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "crops"
    ) -> Dict[str, Any]:
        meta = validate_image_file(file_bytes, content_type)
        ext = filename.split(".")[-1] if "." in filename else "jpg"
        clean_name = f"{folder}_{uuid.uuid4().hex[:10]}.{ext}"
        filepath = os.path.join(self.upload_dir, clean_name)

        with open(filepath, "wb") as f:
            f.write(file_bytes)

        logger.info(f"Saved image to local storage: {filepath}")
        return {
            "url": f"/uploads/{clean_name}",
            "public_id": clean_name,
            "storage_provider": "local",
            "metadata": meta
        }

    async def delete_file(self, public_id: str) -> bool:
        filepath = os.path.join(self.upload_dir, public_id)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                logger.error(f"Failed to delete local file {filepath}: {e}")
        return False

    async def get_file_url(self, public_id: str) -> str:
        return f"/uploads/{public_id}"

    async def generate_signed_url(self, public_id: str, expires_in: int = 3600) -> str:
        return f"/uploads/{public_id}?token={uuid.uuid4().hex[:12]}"


def get_storage_provider() -> StorageProvider:
    provider = (settings.STORAGE_PROVIDER or "cloudinary").lower()
    if provider == "cloudinary":
        return CloudinaryStorageProvider()
    elif provider in ["s3", "aws"]:
        return S3StorageProvider()
    return LocalStorageProvider()

storage_service = get_storage_provider()
