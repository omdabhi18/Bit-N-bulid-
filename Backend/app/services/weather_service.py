from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

from app.models.farm import Farm
from app.models.weather import WeatherRecord
from app.integrations.weather_provider import get_weather_provider, WeatherProvider
from app.integrations.redis_cache import cache_service
from app.integrations.mock_iot import mock_iot_service
from app.schemas.weather import (
    WeatherForecastResponse,
    WeatherCurrent,
    HourlyForecastItem,
    WeatherWindowResponse
)
from app.utils.logger import logger

class WeatherService:
    def __init__(self):
        self.provider: WeatherProvider = get_weather_provider()

    async def _get_farm_coordinates(self, db: Optional[AsyncSession], farm_id: str) -> tuple[float, float, str]:
        if db:
            res = await db.execute(select(Farm).where(Farm.id == farm_id))
            farm = res.scalars().first()
            if farm and farm.latitude and farm.longitude:
                loc = f"{farm.village or 'Ribda'}, {farm.district or 'Rajkot'}"
                return farm.latitude, farm.longitude, loc
        # Default coordinates for GreenValley Smart Farms (Rajkot, Gujarat)
        return 21.9619, 70.7923, "Rajkot, Gujarat"

    async def get_forecast(
        self,
        db: Optional[AsyncSession] = None,
        farm_id: str = "farm-greenvalley-01"
    ) -> WeatherForecastResponse:
        lat, lng, location_name = await self._get_farm_coordinates(db, farm_id)
        cache_key = f"weather:forecast:{lat:.4f}:{lng:.4f}"

        # 1. Try Redis cache
        cached = await cache_service.get(cache_key)
        if cached:
            return WeatherForecastResponse(**cached)

        # 2. Query provider with graceful fallback
        try:
            raw_data = await self.provider.get_forecast(lat, lng)
        except Exception as e:
            logger.warning(f"Weather provider error: {e}. Using fallback provider.")
            from app.integrations.weather_provider import MockWeatherProvider
            raw_data = await MockWeatherProvider().get_forecast(lat, lng)

        # 3. Store in Redis cache (30 min TTL)
        await cache_service.set(cache_key, raw_data, ttl_seconds=1800)

        # 4. Persist historical snapshot in DB if session provided
        if db:
            try:
                cur = raw_data.get("current", {})
                rec = WeatherRecord(
                    id=f"wt-{uuid.uuid4().hex[:6]}",
                    location=location_name,
                    temp=cur.get("temp", 33.0),
                    condition=cur.get("condition", "Partly Cloudy"),
                    humidity=cur.get("humidity", 58.0),
                    wind=cur.get("wind", "14 km/h SW"),
                    rainfall_prob=cur.get("rainfallProb", 12),
                    uv_index=cur.get("uvIndex", 8),
                    dew_point=cur.get("dewPoint", 22.0),
                    et0=cur.get("et0", "5.8 mm/day"),
                    advisory=cur.get("advisory", ""),
                    hourly_forecast=raw_data.get("hourly", []),
                    daily_forecast=raw_data.get("daily", []),
                    updated_at=datetime.now(timezone.utc)
                )
                db.add(rec)
                await db.commit()
            except Exception as e:
                logger.warning(f"Failed to persist weather record: {e}")
                await db.rollback()

        return WeatherForecastResponse(**raw_data)

    async def get_current(
        self,
        db: Optional[AsyncSession] = None,
        farm_id: str = "farm-greenvalley-01"
    ) -> WeatherCurrent:
        fc = await self.get_forecast(db, farm_id)
        return fc.current

    async def get_hourly(
        self,
        db: Optional[AsyncSession] = None,
        farm_id: str = "farm-greenvalley-01"
    ) -> List[HourlyForecastItem]:
        fc = await self.get_forecast(db, farm_id)
        return fc.hourly

    async def get_irrigation_weather_window(
        self,
        db: Optional[AsyncSession] = None,
        farm_id: str = "farm-greenvalley-01"
    ) -> WeatherWindowResponse:
        """
        Synthesizes:
        soil moisture + crop stage + rain probability + temperature + weather window
        Answers: 'Should irrigation happen now?'
        """
        lat, lng, _ = await self._get_farm_coordinates(db, farm_id)
        fc = await self.get_forecast(db, farm_id)
        cur = fc.current

        # Live telemetry
        telemetry = mock_iot_service.get_current_telemetry()
        soil_moisture = float(telemetry.get("soilMoisture", 31.4))
        crop_stage = "Flowering & Boll Formation (કપાસ - ફૂલ અવસ્થા)"

        rain_prob = cur.rainfallProb
        temp = cur.temp
        wind_speed_str = cur.wind

        # Decision matrix
        if rain_prob >= 35:
            should_irrigate = False
            confidence = 88
            rec = "Natural precipitation predicted (>35%). Hold off irrigation to prevent root hypoxia and water wastage."
            rec_gu = "વરસાદની શક્યતા વધુ હોવાથી અત્યારે પિયત મોકૂફ રાખો."
            best_window = "Post-rain inspection"
        elif soil_moisture >= 45.0:
            should_irrigate = False
            confidence = 94
            rec = f"Root-zone moisture is sufficient ({soil_moisture}%). No irrigation required today."
            rec_gu = f"જમીનમાં પૂરતો ભેજ ({soil_moisture}%) છે. આજે પિયતની જરૂર નથી."
            best_window = "Check in 48 hours"
        elif soil_moisture < 35.0:
            should_irrigate = True
            confidence = 92
            rec = (
                f"Root-zone moisture is critically low ({soil_moisture}%) during sensitive {crop_stage}. "
                f"Rain probability is minimal ({rain_prob}%). Execute 35-minute drip irrigation between 18:00 - 19:30 IST."
            )
            rec_gu = f"કપાસના ફૂલ અવસ્થામાં જમીનનો ભેજ ({soil_moisture}%) ઘણો ઓછો છે. આજે સાંજે ૬:૦૦ વાગ્યે ડ્રિપ પિયત આપવું જરૂરી છે."
            best_window = "Today • 18:00 - 19:30 IST"
        else:
            should_irrigate = False
            confidence = 82
            rec = f"Soil moisture ({soil_moisture}%) is in maintenance range. Evening watering optional."
            rec_gu = "ભેજ સામાન્ય સ્થિતિમાં છે."
            best_window = "Tomorrow Morning"

        return WeatherWindowResponse(
            shouldIrrigateNow=should_irrigate,
            confidence=confidence,
            recommendation=rec,
            recommendationGu=rec_gu,
            factors={
                "soilMoisture": f"{soil_moisture}%",
                "cropStage": crop_stage,
                "rainProbability": f"{rain_prob}%",
                "temperature": f"{temp}°C",
                "wind": wind_speed_str
            },
            bestWindow=best_window,
            windSpeed=wind_speed_str,
            rainProbability=rain_prob,
            currentTemperature=temp
        )

weather_service = WeatherService()
