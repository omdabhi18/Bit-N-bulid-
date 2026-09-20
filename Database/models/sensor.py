import enum
import uuid
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Database.connection import Base


class SensorType(str, enum.Enum):
    SOIL_MOISTURE = "SOIL_MOISTURE"
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    PH = "PH"
    NITROGEN = "NITROGEN"
    PHOSPHORUS = "PHOSPHORUS"
    POTASSIUM = "POTASSIUM"

class SensorStatus(str, enum.Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    STANDBY = "STANDBY"
    ACTIVE = "ACTIVE"

class Sensor(Base):

    __tablename__ = "sensors"

    id = Column(String(50), primary_key=True, default=lambda: f"sns-{uuid.uuid4().hex[:4]}") # e.g. "SN-Cotton-01"
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)
    device_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(120), default="IoT Field Sensor")

    sensor_type = Column(String(50), default="SOIL_MOISTURE")
    battery = Column(Integer, default=95)
    signal_strength = Column(String(50), default="Excellent (4G IoT)")
    status = Column(String(30), default="ONLINE") # ONLINE | OFFLINE | STANDBY
    last_seen = Column(String(50), default="Just now")
    configuration = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    farm = relationship("Farm", back_populates="sensors")
    field = relationship("Field", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")
