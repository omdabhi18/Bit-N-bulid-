from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)
    name = Column(String, default="GreenValley Smart Farms")
    farmer_name = Column(String, default="Kishanbhai Patel")
    village = Column(String, default="Ribda")
    taluka = Column(String, default="Gondal")
    district = Column(String, default="Rajkot")
    state = Column(String, default="Gujarat")
    total_area_acre = Column(Float, default=12.5)
    soil_type = Column(String, default="Medium Black Clayey Loam (કાળી જમીન)")
    irrigation_method = Column(String, default="Drip Automation + Tube Well")
    latitude = Column(Float, default=21.9619)
    longitude = Column(Float, default=70.7923)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="farms")
    fields = relationship("Field", back_populates="farm", cascade="all, delete-orphan")
    sensors = relationship("SensorNode", back_populates="farm", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="farm", cascade="all, delete-orphan")
    advisories = relationship("AIAdvisory", back_populates="farm", cascade="all, delete-orphan")
    action_plans = relationship("ActionPlan", back_populates="farm", cascade="all, delete-orphan")
    tasks = relationship("FarmTask", back_populates="farm", cascade="all, delete-orphan")

class Field(Base):
    __tablename__ = "fields"

    id = Column(String, primary_key=True) # e.g. "field-a"
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    name = Column(String, nullable=False)
    crop = Column(String, nullable=False)
    area = Column(String, default="5.0 Acres")
    stage = Column(String, default="Flowering")
    health_score = Column(Integer, default=80)
    soil_moisture = Column(Float, default=35.0)
    status = Column(String, default="Warning") # Healthy | Warning | Critical
    risk_category = Column(String, default="Water Stress")
    pest_risk = Column(String, default="Low (15%)")
    soil_ph = Column(Float, default=6.8)
    nitrogen = Column(String, default="Normal")
    phosphorus = Column(String, default="Optimal")
    potassium = Column(String, default="High")
    sensor_node = Column(String, default="SN-Cotton-01")
    sensor_status = Column(String, default="Online")
    coordinates = Column(JSON, default=list) # [{lat, lng}, ...]
    color = Column(String, default="#eab308")
    drip_status = Column(String, default="Ready")
    recommendation = Column(String, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="fields")
