import enum
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class NotificationType(str, enum.Enum):
    ACTION_REQUIRED = "ACTION_REQUIRED"
    RISK_WARNING = "RISK_WARNING"
    TASK_UPDATE = "TASK_UPDATE"
    SYSTEM_INFO = "SYSTEM_INFO"

class NotificationChannel(str, enum.Enum):
    WEB = "WEB"
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    EMAIL = "EMAIL"

class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    type = Column(String(50), default="ACTION_REQUIRED")
    channel = Column(String(30), default="WEB") # WEB | SMS | WHATSAPP | EMAIL
    title = Column(String(200), nullable=False)
    message = Column(String(500), nullable=False)
    status = Column(String(30), default="SENT") # PENDING | SENT | FAILED
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationship
    user = relationship("User", back_populates="notifications")
