from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey, DateTime
from datetime import datetime, timezone
import uuid
from app.database import Base

class DiseaseAnalysis(Base):
    __tablename__ = "disease_analyses"

    id = Column(String, primary_key=True, default=lambda: f"dis-{uuid.uuid4().hex[:4]}")
    crop_id = Column(String, nullable=True, index=True)
    field_id = Column(String, nullable=True, index=True)
    crop = Column(String, nullable=False)
    disease = Column(String, default="Disease")
    disease_name = Column(String, nullable=False)
    disease_name_gu = Column(String, nullable=True)
    pest = Column(String, nullable=True)
    confidence = Column(Integer, default=85)
    severity = Column(String, default="High")
    image_url = Column(String, nullable=False)
    storage_provider = Column(String, default="cloudinary")
    public_id = Column(String, default="")
    image_metadata = Column(JSON, default=dict)
    analysis = Column(String, default="")
    symptoms = Column(JSON, default=list)
    recommendation = Column(String, default="")
    recommended_remedy = Column(JSON, default=dict) # { organic, chemical, prevention }
    expert_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ExpertReviewTicket(Base):
    __tablename__ = "expert_review_tickets"

    id = Column(String, primary_key=True, default=lambda: f"ESC-{uuid.uuid4().hex[:3].upper()}")
    field = Column(String, default="Field B (Wheat)")
    crop = Column(String, default="Wheat")
    issue = Column(String, nullable=False)
    ai_confidence = Column(Integer, default=58)
    reason = Column(String, default="")
    assigned_agronomist = Column(String, default="Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)")
    status = Column(String, default="Review Pending")
    submitted_at = Column(String, default="Just now")
    telemetry_snapshot = Column(JSON, default=dict)
    agronomist_notes = Column(String, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
