import enum
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class ExpertRequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    REVIEW_PENDING = "REVIEW_PENDING"
    IN_REVIEW = "IN_REVIEW"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"

class ExpertRequest(Base):

    __tablename__ = "expert_requests"

    id = Column(String(50), primary_key=True, default=lambda: f"ESC-{uuid.uuid4().hex[:3].upper()}")
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    disease_analysis_id = Column(String(50), ForeignKey("disease_analyses.id", ondelete="SET NULL"), nullable=True, index=True)
    risk_id = Column(String(50), ForeignKey("risks.id", ondelete="SET NULL"), nullable=True, index=True)
    requested_by = Column(String(120), default="Kishanbhai Patel")
    assigned_expert = Column(String(150), default="Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)")
    field_name = Column(String(100), default="Field B (Wheat)")
    crop = Column(String(100), default="Wheat")
    issue = Column(String(255), default="Agronomic Expert Review Needed", nullable=True)

    ai_confidence = Column(Integer, default=58)
    reason = Column(String(500), default="")
    status = Column(String(30), default="REVIEW_PENDING", index=True) # REVIEW_PENDING | IN_REVIEW | RESOLVED
    expert_response = Column(String(1000), default="")
    agronomist_notes = Column(String(1000), default="")
    telemetry_snapshot = Column(JSON, default=dict)
    submitted_at = Column(String(50), default="Just now")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    field = relationship("Field", back_populates="expert_requests")
    disease_analysis = relationship("DiseaseAnalysis", back_populates="expert_requests")
