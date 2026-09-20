from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from datetime import datetime, timezone
import uuid
from app.database import Base

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location = Column(String, default="Rajkot, Gujarat")
    temp = Column(Float, default=33.0)
    condition = Column(String, default="Mostly Sunny")
    humidity = Column(Float, default=58.0)
    wind = Column(String, default="14 km/h SW")
    rainfall_prob = Column(Integer, default=12)
    uv_index = Column(Integer, default=8)
    dew_point = Column(Float, default=22.0)
    et0 = Column(String, default="5.8 mm/day")
    advisory = Column(String, default="Favorable conditions for drip irrigation this evening.")
    hourly_forecast = Column(JSON, default=list) # [{time, temp, rainProb, humidity}]
    daily_forecast = Column(JSON, default=list)  # [{day, tempMax, tempMin, rainProb, condition, sprayRating}]
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
