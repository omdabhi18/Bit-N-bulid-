from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Database.connection import Base
import enum
import uuid


class CropStage(str, enum.Enum):
    GERMINATION = "Germination"
    VEGETATIVE = "Vegetative"
    FLOWERING = "Flowering"
    BOLL_FORMATION = "Boll Formation"
    GRAIN_FILLING = "Grain Filling"
    POD_DEVELOPMENT = "Pod Development"
    MATURITY = "Maturity"
    HARVESTED = "Harvested"

class HealthStatus(str, enum.Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    ATTENTION_REQUIRED = "Attention Required"
    POOR = "Poor"

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String(50), primary_key=True, default=lambda: f"crop-{uuid.uuid4().hex[:4]}") # e.g. "cotton", "wheat"
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(100), nullable=True, index=True)
    crop_name = Column(String(100), nullable=True)
    name_gujarati = Column(String(120), nullable=True, index=True)
    category = Column(String(100), default="Cash Crop", index=True)
    scientific_name = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    disease_ai_supported = Column(Boolean, default=False, index=True)
    variety = Column(String(100), default="High Yield Hybrid")
    sowing_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expected_harvest_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    current_stage = Column(String(100), default="Vegetative")
    stage = Column(String(100), default="Vegetative")
    health_status = Column(String(50), default="Good")
    area = Column(Float, default=5.0)
    field_name = Column(String(100), default="Field A")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        if "name" in kwargs and "crop_name" not in kwargs:
            kwargs["crop_name"] = kwargs["name"]
        elif "crop_name" in kwargs and "name" not in kwargs:
            kwargs["name"] = kwargs["crop_name"]
        if "stage" in kwargs and "current_stage" not in kwargs:
            kwargs["current_stage"] = kwargs["stage"]
        elif "current_stage" in kwargs and "stage" not in kwargs:
            kwargs["stage"] = kwargs["current_stage"]
        super().__init__(**kwargs)



    # Relationships
    farm = relationship("Farm", back_populates="crops")
    field = relationship("Field", back_populates="crops")
