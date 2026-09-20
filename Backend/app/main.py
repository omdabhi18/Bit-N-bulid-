import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.database import engine, Base, AsyncSessionLocal
from app.api import api_router
from app.integrations.websocket_manager import ws_manager
from app.integrations.mqtt_client import mqtt_service
from app.utils.seed_data import seed_database
from app.utils.logger import logger
from app.workers.scheduler import periodic_telemetry_jitter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing KrishiNetra AI Backend...")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # 1. Initialize Database Tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema initialized.")

    # 2. Seed Initial Realistic Farm Data
    async with AsyncSessionLocal() as session:
        await seed_database(session)

    # 3. Start MQTT Client (or Mock IoT Fallback)
    mqtt_service.start()

    # 4. Start Background Scheduler Task
    scheduler_task = asyncio.create_task(periodic_telemetry_jitter("farm-greenvalley-01"))

    yield

    # Shutdown
    scheduler_task.cancel()
    mqtt_service.stop()
    await engine.dispose()
    logger.info("KrishiNetra AI Backend shutdown cleanly.")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Autonomous Farm-to-Field Advisory & Action Orchestration Agent Backend",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads Static Directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# WebSocket Endpoint
@app.websocket("/ws/farm/{farm_id}")
async def websocket_farm_endpoint(websocket: WebSocket, farm_id: str):
    await ws_manager.connect(farm_id, websocket)
    try:
        while True:
            # Keep-alive receive loop
            data = await websocket.receive_text()
            logger.debug(f"Received from WebSocket client: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(farm_id, websocket)
    except Exception as e:
        logger.warning(f"WebSocket exception: {e}")
        ws_manager.disconnect(farm_id, websocket)

# Global Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": {}
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "details": {"errors": exc.errors()}
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please check server logs.",
                "details": {}
            }
        }
    )

# Root Health Check
@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "farm": "GreenValley Smart Farms (Rajkot, Gujarat)"
    }

# Include API Router
app.include_router(api_router)
