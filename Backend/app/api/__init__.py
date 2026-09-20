from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.farms import router as farms_router
from app.api.crops import router as crops_router
from app.api.sensors import router as sensors_router
from app.api.monitoring import router as monitoring_router
from app.api.risks import router as risks_router
from app.api.advisory import router as advisory_router
from app.api.action_plans import router as action_plans_router
from app.api.tasks import router as tasks_router
from app.api.agents import router as agents_router
from app.api.disease import router as disease_router
from app.api.weather import router as weather_router
from app.api.market import router as market_router
from app.api.voice import router as voice_router
from app.api.notifications import router as notifications_router
from app.api.reports import router as reports_router
from app.api.storage import router as storage_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(dashboard_router)
api_router.include_router(farms_router)
api_router.include_router(crops_router)
api_router.include_router(sensors_router)
api_router.include_router(monitoring_router)
api_router.include_router(risks_router)
api_router.include_router(advisory_router)
api_router.include_router(action_plans_router)
api_router.include_router(tasks_router)
api_router.include_router(agents_router)
api_router.include_router(disease_router)
api_router.include_router(weather_router)
api_router.include_router(market_router)
api_router.include_router(voice_router)
api_router.include_router(notifications_router)
api_router.include_router(reports_router)
api_router.include_router(storage_router)

__all__ = ["api_router"]
