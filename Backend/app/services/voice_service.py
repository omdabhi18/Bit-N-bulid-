from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.integrations.llm_client import get_llm_provider, LLMProvider
from app.integrations.speech_to_text import get_stt_provider, SpeechToTextProvider
from app.integrations.text_to_speech import get_tts_provider, TextToSpeechProvider
from app.integrations.mock_iot import mock_iot_service
from app.models.farm import Farm, Field
from app.models.sensor import SensorReading
from app.models.risk import Risk
from app.models.task import FarmTask
from app.schemas.voice import VoiceQueryRequest, VoiceQueryResponse
from app.utils.logger import logger

class VoiceService:
    def __init__(self):
        self.llm: LLMProvider = get_llm_provider()
        self.stt: SpeechToTextProvider = get_stt_provider()
        self.tts: TextToSpeechProvider = get_tts_provider()

    async def retrieve_farm_context(
        self,
        db: Optional[AsyncSession],
        farm_id: str = "farm-greenvalley-01",
        field_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gathers comprehensive live farm context:
        - Field details
        - Current soil moisture
        - Crop & crop stage
        - Weather & rain probability
        - Active agronomic risks
        - Recent irrigation history
        """
        # Baseline from real-time telemetry
        live_telemetry = mock_iot_service.get_current_telemetry()
        
        context = {
            "farm_id": farm_id,
            "field_name": "Field A (Cotton)",
            "soilMoisture": live_telemetry.get("soilMoisture", 31.4),
            "soilTemperature": live_telemetry.get("soilTemperature", 27.8),
            "airHumidity": live_telemetry.get("airHumidity", 58.0),
            "rainfallProb24h": live_telemetry.get("rainfallProb24h", 12),
            "farmHealthScore": live_telemetry.get("farmHealthScore", 82),
            "crop": "BT Cotton (કપાસ)",
            "cropStage": "Flowering & Boll Formation",
            "activeRisks": ["Soil Moisture Deficit (31.4%)", "Low Phosphorus (14 mg/kg)"],
            "recentIrrigation": "Last cycle 4 days ago (30 mins)",
            "weatherSummary": "Hot & Dry (33.2°C), 14 km/h wind, clear evening window"
        }

        if not db:
            return context

        try:
            # 1. Field & Crop stage retrieval
            res = await db.execute(select(Field).where(Field.farm_id == farm_id))
            fields = res.scalars().all()
            if fields:
                field = fields[0]
                context["field_name"] = field.name
                context["crop"] = field.crop_type or field.crop or context["crop"]

            # 2. Latest sensor reading
            s_res = await db.execute(
                select(SensorReading)
                .order_by(SensorReading.timestamp.desc())
                .limit(1)
            )
            latest_reading = s_res.scalars().first()
            if latest_reading and latest_reading.soil_moisture:
                context["soilMoisture"] = latest_reading.soil_moisture
                context["soilTemperature"] = latest_reading.soil_temperature

            # 3. Active risks from database
            r_res = await db.execute(select(Risk).where(Risk.status == "active"))
            risks = r_res.scalars().all()
            if risks:
                context["activeRisks"] = [f"{r.title} ({r.severity})" for r in risks]

            # 4. Recent irrigation task
            t_res = await db.execute(
                select(FarmTask)
                .where(FarmTask.farm_id == farm_id)
                .order_by(FarmTask.created_at.desc())
                .limit(1)
            )
            latest_task = t_res.scalars().first()
            if latest_task:
                context["recentIrrigation"] = f"{latest_task.title} - Status: {latest_task.status}"

        except Exception as e:
            logger.warning(f"Error compiling DB farm context for voice query: {e}. Using live memory state.")

        return context

    async def handle_voice_query(
        self,
        db: Optional[AsyncSession],
        farm_id: str,
        request: VoiceQueryRequest
    ) -> VoiceQueryResponse:
        # Step 1: Farm Context Retrieval
        farm_context = await self.retrieve_farm_context(db, farm_id, request.query)

        # Step 2: Query LLM with grounded farm context
        result = await self.llm.answer_kisan_query(
            query=request.query,
            farm_context=farm_context,
            language=request.language
        )

        reply_text = result.get("reply", "No response generated.")
        audio_url = None

        # Step 3: Text-to-Speech synthesis
        try:
            tts_res = await self.tts.synthesize(reply_text, language=request.language)
            audio_url = tts_res.get("audio_url")
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}. Gracefully returning text response.")

        return VoiceQueryResponse(
            query=request.query,
            language=request.language,
            replyText=reply_text,
            actionRecommendation=result.get("action"),
            audioUrl=audio_url,
            telemetryFactorsUsed=result.get("factors", [
                f"Moisture: {farm_context.get('soilMoisture')}%",
                f"Rain: {farm_context.get('rainfallProb24h')}%"
            ])
        )

    async def transcribe_audio(self, audio_bytes: bytes, language: str = "gu") -> Dict[str, Any]:
        """Convert incoming farmer speech audio to text."""
        return await self.stt.transcribe(audio_bytes, language=language)

voice_service = VoiceService()
