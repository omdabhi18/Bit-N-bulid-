from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone
from app.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String, primary_key=True) # e.g. "cotton", "wheat", "groundnut"
    farm_id = Column(String, ForeignKey("farms.id"), nullable=True)
    name = Column(String, nullable=False, index=True)
    name_gujarati = Column(String, nullable=True, index=True)
    category = Column(String, default="Cash Crop", index=True)
    scientific_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    disease_ai_supported = Column(Boolean, default=False, index=True)
    variety = Column(String, default="High Yield Hybrid")
    stage = Column(String, default="Vegetative")
    area = Column(Float, default=5.0)
    field_name = Column(String, default="Field A")
    sowing_date = Column(String, default="2026-06-15")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

