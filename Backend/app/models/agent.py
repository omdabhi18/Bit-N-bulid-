from sqlalchemy import Column, String, Integer, JSON, DateTime
from datetime import datetime, timezone
import uuid
from app.database import Base

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_name = Column(String(50), nullable=False, index=True)
    field_id = Column(String(50), nullable=True, index=True)
    role = Column(String(150), default="Autonomous Agriculture Agent")
    status = Column(String(30), default="COMPLETED", index=True) # ACTIVE | COMPLETED | FAILED
    confidence = Column(Integer, default=95)
    input_summary = Column(JSON, default=dict)
    output_summary = Column(JSON, default=dict)

    inputs = Column(JSON, default=list)
    outputs = Column(JSON, default=list)
    execution_time_ms = Column(Integer, default=120)
    error_message = Column(String(500), nullable=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
