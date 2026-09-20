from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "KrishiNetra AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_STR: str = "/api"

    # Security
    SECRET_KEY: str = "krishinetra-super-secret-key-change-in-production-2026!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{(Path(__file__).resolve().parent.parent.parent / 'krishinetra.db').as_posix()}"
    SYNC_DATABASE_URL: str = f"sqlite:///{(Path(__file__).resolve().parent.parent.parent / 'krishinetra.db').as_posix()}"

    # MQTT & IoT
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    MQTT_KEEPALIVE: int = 60
    USE_MOCK_IOT: bool = True

    # AI & Providers
    AI_PROVIDER: str = "mock"  # mock | gemini | openai
    LLM_PROVIDER: str = "mock" # mock | gemini | openai
    LLM_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Weather
    WEATHER_PROVIDER: str = "openmeteo" # openmeteo | mock
    WEATHER_API_KEY: Optional[str] = None

    # Mandi / Market Prices
    MARKET_PROVIDER: str = "agmarknet" # agmarknet | mock
    MARKET_API_KEY: Optional[str] = None

    # Storage
    STORAGE_PROVIDER: str = "local" # local | cloudinary | s3
    UPLOAD_DIR: str = "./uploads"
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_BUCKET_NAME: Optional[str] = None
    AWS_REGION: str = "ap-south-1"

    # Voice AI (STT & TTS)
    VOICE_STT_PROVIDER: str = "webspeech" # webspeech | whisper | mock
    VOICE_STT_API_KEY: Optional[str] = None
    VOICE_TTS_PROVIDER: str = "browser" # browser | google | openai | mock
    VOICE_TTS_API_KEY: Optional[str] = None

    # Redis & Background
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

settings = Settings()
