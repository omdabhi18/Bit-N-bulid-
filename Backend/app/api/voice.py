from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any

from app.database import get_db
from app.services.voice_service import voice_service
from app.schemas.voice import VoiceQueryRequest, VoiceQueryResponse

router = APIRouter(prefix="/voice", tags=["Kisan Voice AI"])

@router.post("/query", response_model=VoiceQueryResponse)
async def query_voice_ai(req: VoiceQueryRequest, db: AsyncSession = Depends(get_db)):
    """Answer farmer natural-language question grounded in live field telemetry."""
    return await voice_service.handle_voice_query(db, "farm-greenvalley-01", req)

@router.post("/transcribe")
async def transcribe_speech(
    file: UploadFile = File(...),
    language: str = Form("gu")
) -> Dict[str, Any]:
    """Transcribe spoken Gujarati, Hindi, or English audio into text."""
    audio_bytes = await file.read()
    return await voice_service.transcribe_audio(audio_bytes, language=language)

@router.post("/synthesize")
async def synthesize_speech(
    text: str = Form(...),
    language: str = Form("gu")
) -> Dict[str, Any]:
    """Convert text answer into vernacular spoken audio file."""
    return await voice_service.tts.synthesize(text=text, language=language)
