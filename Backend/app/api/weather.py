from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.weather_service import weather_service
from app.schemas.weather import (
    WeatherForecastResponse,
    WeatherCurrent,
    HourlyForecastItem,
    WeatherWindowResponse
)

router = APIRouter(prefix="/weather", tags=["Weather Intelligence"])

@router.get("", response_model=WeatherForecastResponse)
async def get_weather_default(db: AsyncSession = Depends(get_db)):
    return await weather_service.get_forecast(db)

@router.get("/forecast", response_model=WeatherForecastResponse)
async def get_weather_forecast(db: AsyncSession = Depends(get_db)):
    return await weather_service.get_forecast(db)

@router.get("/current", response_model=WeatherCurrent)
async def get_current_weather(db: AsyncSession = Depends(get_db)):
    return await weather_service.get_current(db)

@router.get("/hourly", response_model=List[HourlyForecastItem])
async def get_hourly_forecast(db: AsyncSession = Depends(get_db)):
    return await weather_service.get_hourly(db)

@router.get("/window", response_model=WeatherWindowResponse)
async def get_irrigation_weather_window(db: AsyncSession = Depends(get_db)):
    return await weather_service.get_irrigation_weather_window(db)
