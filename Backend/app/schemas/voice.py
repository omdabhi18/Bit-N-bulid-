from pydantic import BaseModel
from typing import Optional, List

class VoiceQueryRequest(BaseModel):
    query: str
    language: str = "gu" # gu | hi | en

class VoiceQueryResponse(BaseModel):
    query: str
    language: str
    replyText: str
    actionRecommendation: Optional[str] = None # irrigate | spray | sell | fertilize | none
    audioUrl: Optional[str] = None
    telemetryFactorsUsed: List[str] = []
