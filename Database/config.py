from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database URLs
    # For PostgreSQL: postgresql+asyncpg://postgres:postgres@localhost:5432/krishinetra_db
    # For SQLite fallback: sqlite+aiosqlite:///./krishinetra.db
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./krishinetra.db")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL", "sqlite:///./krishinetra.db")

    # Connection Pooling settings
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800 # 30 minutes
    DB_ECHO: bool = False

    # Redis URL for caching / job state
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

db_settings = DatabaseSettings()
