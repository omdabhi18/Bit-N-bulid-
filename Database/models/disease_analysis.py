from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class DiseaseAnalysis(Base):
    __tablename__ = "disease_analyses"

    id = Column(String(50), primary_key=True, default=lambda: f"dis-{uuid.uuid4().hex[:4]}")
    crop_id = Column(String(50), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    crop = Column(String(100), default="Cotton")

    disease = Column(String(150), nullable=False)
    disease_name = Column(String(150), default="Leaf Blight")

    disease_name_gu = Column(String(150), nullable=True)
    pest = Column(String(150), nullable=True)
    confidence = Column(Integer, default=85)
    severity = Column(String(30), default="High")
    image_url = Column(String(500), nullable=False)
    storage_provider = Column(String(50), default="cloudinary")
    public_id = Column(String(255), default="")
    image_metadata = Column(JSON, default=dict)
    analysis = Column(String(1000), default="")
    symptoms = Column(JSON, default=list)
    recommendation = Column(String(1000), default="")
    recommended_remedy = Column(JSON, default=dict)
    expert_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    field = relationship("Field", back_populates="disease_analyses")
    expert_requests = relationship("ExpertRequest", back_populates="disease_analysis")
