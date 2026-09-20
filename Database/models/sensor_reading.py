from sqlalchemy import Column, String, Float, JSON, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = Column(String(50), ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True)
    field_id = Column(String(50), nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    soil_moisture = Column(Float, default=31.4)
    soil_temperature = Column(Float, default=27.8)
    soil_ph = Column(Float, default=6.8)
    soil_ec = Column(Float, default=0.42)
    nitrogen = Column(Float, default=82.0)
    phosphorus = Column(Float, default=14.0)
    potassium = Column(Float, default=185.0)
    air_temperature = Column(Float, default=33.2)
    air_humidity = Column(Float, default=58.0)
    value = Column(Float, nullable=True)
    unit = Column(String(30), default="%")
    reading_metadata = Column(JSON, default=dict)

    # Composite index for lightning-fast time-series queries
    __table_args__ = (
        Index("idx_sensor_readings_sensor_timestamp", "sensor_id", "timestamp"),
    )

    # Relationship
    sensor = relationship("Sensor", back_populates="readings")
