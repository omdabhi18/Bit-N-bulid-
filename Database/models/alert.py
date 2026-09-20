import enum
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class AlertType(str, enum.Enum):
    WATER_DEFICIT = "WATER_DEFICIT"
    PEST_ALERT = "PEST_ALERT"
    DISEASE_OUTBREAK = "DISEASE_OUTBREAK"
    EQUIPMENT_FAULT = "EQUIPMENT_FAULT"
    WEATHER_WARNING = "WEATHER_WARNING"

class AlertSeverity(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    type = Column(String(50), default="WATER_DEFICIT")
    severity = Column(String(30), default="WARNING") # INFO | WARNING | CRITICAL
    title = Column(String(200), nullable=False)
    message = Column(String(500), nullable=False)
    read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    user = relationship("User", back_populates="alerts")
    field = relationship("Field", back_populates="alerts")
