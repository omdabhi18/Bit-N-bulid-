from sqlalchemy import Column, String, ForeignKey, DateTime
from datetime import datetime, timezone
import uuid
from app.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(String, primary_key=True, default=lambda: f"LOG-{uuid.uuid4().hex[:4].upper()}")
    farm_id = Column(String, nullable=True)
    time = Column(String, default="Just now")
    agent = Column(String, nullable=False) # e.g. "Master Orchestrator", "Execution Agent"
    event = Column(String, nullable=False)
    severity = Column(String, default="info") # info | success | warning | error
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AlertNotification(Base):
    __tablename__ = "alert_notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = Column(String, nullable=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(String, default="warning")
    is_read = Column(String, default="unread")
    channel = Column(String, default="web") # web | sms | whatsapp | email
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
