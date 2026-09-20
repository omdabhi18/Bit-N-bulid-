import base64
import logging
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.config import settings

logger = logging.getLogger(__name__)

class SpeechToTextProvider(ABC):
    """Abstract Base Class for Speech-to-Text Providers."""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, language: str = "gu") -> Dict[str, Any]:
        """Transcribe speech audio bytes into text."""
        pass


class GoogleSpeechToTextProvider(SpeechToTextProvider):
    """Google Cloud Speech-to-Text Provider with Indian Vernacular Language Support."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.VOICE_STT_API_KEY
        self.endpoint = "https://speech.googleapis.com/v1/speech:recognize"
        self._fallback = MockSpeechToTextProvider()

    def _lang_code(self, lang: str) -> str:
        mapping = {
            "gu": "gu-IN",
            "hi": "hi-IN",
            "en": "en-IN"
        }
        return mapping.get(lang.lower(), "gu-IN")

    async def transcribe(self, audio_bytes: bytes, language: str = "gu") -> Dict[str, Any]:
        if not self.api_key or self.api_key in ["mock_key", "your_voice_stt_api_key"]:
            return await self._fallback.transcribe(audio_bytes, language)

        lang_code = self._lang_code(language)
        payload = {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": 16000,
                "languageCode": lang_code,
                "enableAutomaticPunctuation": True
            },
            "audio": {
                "content": base64.b64encode(audio_bytes).decode("utf-8")
            }
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(f"{self.endpoint}?key={self.api_key}", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    results = data.get("results", [])
                    if results:
                        transcription = results[0]["alternatives"][0]["transcript"]
                        confidence = results[0]["alternatives"][0].get("confidence", 0.95)
                        return {
                            "text": transcription,
                            "language": language,
                            "confidence": confidence,
                            "provider": "google_speech"
                        }
        except Exception as e:
            logger.warning(f"Google STT failed: {e}. Falling back to mock transcriber.")

        return await self._fallback.transcribe(audio_bytes, language)


class MockSpeechToTextProvider(SpeechToTextProvider):
    """Mock STT Provider for reliable development and offline testing."""

    async def transcribe(self, audio_bytes: bytes, language: str = "gu") -> Dict[str, Any]:
        # Return realistic vernacular farmer questions
        if language == "gu":
            text = "Mara Field A ma aaje pani aapvu joie?"
        elif language == "hi":
            text = "Khet A mein aaj paani dena hai kya?"
        else:
            text = "Should I irrigate Field A today?"

        return {
            "text": text,
            "language": language,
            "confidence": 0.96,
            "provider": "mock_speech"
        }


def get_stt_provider() -> SpeechToTextProvider:
    provider = (settings.VOICE_STT_PROVIDER or "mock").lower()
    if provider in ["google", "gcp"]:
        return GoogleSpeechToTextProvider()
    return MockSpeechToTextProvider()

stt_service = get_stt_provider()
