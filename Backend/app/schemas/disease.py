from pydantic import BaseModel
from typing import List, Optional, Dict

class DiseaseRemedy(BaseModel):
    organic: str
    chemical: str
    prevention: str

class DiseaseCatalogItem(BaseModel):
    id: str
    crop: str
    diseaseName: str
    diseaseNameGu: Optional[str] = None
    confidence: int
    severity: str
    image: str
    symptoms: List[str]
    recommendedRemedy: DiseaseRemedy

class DiseaseAnalyzeResponse(BaseModel):
    id: str
    crop: str
    crop_id: Optional[str] = None
    diseaseName: str
    diseaseNameGu: Optional[str] = None
    confidence: int
    severity: str
    imageUrl: str
    symptoms: List[str]
    recommendedRemedy: DiseaseRemedy
    requiresExpertEscalation: bool = False
    supported: bool = True
    message: Optional[str] = None

class EscalationCreateRequest(BaseModel):
    field: str
    crop: str
    crop_id: Optional[str] = None
    disease_analysis_id: Optional[str] = None
    issue: str
    aiConfidence: int
    reason: str
    telemetrySnapshot: Optional[Dict[str, str]] = None

class EscalationResponse(BaseModel):
    id: str
    field: str
    crop: str
    issue: str
    aiConfidence: int
    reason: str
    assignedAgronomist: str
    status: str
    submittedAt: str
    telemetrySnapshot: Dict[str, str]
    agronomistNotes: str
