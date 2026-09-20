from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)

    location = Column(String(120), default="Rajkot, Gujarat")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    temperature = Column(Float, default=33.0)
    humidity = Column(Float, default=58.0)
    rainfall_probability = Column(Integer, default=12)
    rainfall = Column(Float, default=0.0)
    wind_speed = Column(Float, default=14.0)
    wind_direction = Column(String(30), default="SW")
    weather_condition = Column(String(100), default="Mostly Sunny")
    uv_index = Column(Integer, default=8)
    dew_point = Column(Float, default=22.0)
    et0 = Column(String(30), default="5.8 mm/day")
    advisory = Column(String(255), default="Favorable conditions for drip irrigation this evening.")
    source = Column(String(50), default="IMD / Hyperlocal Station")
    hourly_forecast = Column(JSON, default=list)
    daily_forecast = Column(JSON, default=list)

    # Relationship
    farm = relationship("Farm", back_populates="weather_records")
