from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class SensorNode(Base):
    __tablename__ = "sensor_nodes"

    id = Column(String, primary_key=True) # e.g. "SN-Cotton-01"
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    name = Column(String, nullable=False)
    field_name = Column(String, default="Field A")
    battery = Column(Integer, default=95)
    signal_strength = Column(String, default="Excellent (4G IoT)")
    status = Column(String, default="Online")
    sensor_type = Column(String, default="FDR Moisture + NPK Probes")
    last_sync = Column(String, default="Just now")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = Column(String, ForeignKey("sensor_nodes.id"), nullable=False)
    field_id = Column(String, nullable=True)
    soil_moisture = Column(Float, default=31.4)
    soil_temperature = Column(Float, default=27.8)
    soil_ph = Column(Float, default=6.8)
    soil_ec = Column(Float, default=0.42)
    nitrogen = Column(Float, default=82.0)
    phosphorus = Column(Float, default=14.0)
    potassium = Column(Float, default=185.0)
    air_temperature = Column(Float, default=33.2)
    air_humidity = Column(Float, default=58.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    sensor = relationship("SensorNode", back_populates="readings")
