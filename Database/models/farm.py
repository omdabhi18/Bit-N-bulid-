from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    farmer_name = Column(String(120), nullable=True, default="Kishanbhai Patel")
    location = Column(String(150), default="Rajkot, Gujarat")
    village = Column(String(100), default="Ribda")
    taluka = Column(String(100), default="Gondal")
    district = Column(String(100), default="Rajkot")
    state = Column(String(100), default="Gujarat")
    latitude = Column(Float, default=21.9619)
    longitude = Column(Float, default=70.7923)
    area = Column(Float, default=12.5) # in acres
    soil_type = Column(String(150), default="Black Cotton")
    irrigation_method = Column(String(150), default="Drip Automation + Tube Well")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", back_populates="farms")
    fields = relationship("Field", back_populates="farm", cascade="all, delete-orphan")
    crops = relationship("Crop", back_populates="farm", cascade="all, delete-orphan")
    sensors = relationship("Sensor", back_populates="farm", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="farm", cascade="all, delete-orphan")
    ai_advisories = relationship("AIAdvisory", back_populates="farm", cascade="all, delete-orphan")
    action_plans = relationship("ActionPlan", back_populates="farm", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="farm", cascade="all, delete-orphan")
    weather_records = relationship("WeatherData", back_populates="farm", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="farm")
