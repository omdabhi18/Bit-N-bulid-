import os
import io
import uuid
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.config import settings

logger = logging.getLogger(__name__)

class TextToSpeechProvider(ABC):
    """Abstract Base Class for Text-to-Speech Providers."""

    @abstractmethod
    async def synthesize(self, text: str, language: str = "gu") -> Dict[str, Any]:
        """Convert text into spoken audio bytes and accessible URL."""
        pass


class GTTSVoiceProvider(TextToSpeechProvider):
    """Google Text-to-Speech integration supporting Gujarati (gu), Hindi (hi), and English (en)."""

    def __init__(self):
        self.audio_dir = os.path.join(settings.UPLOAD_DIR, "audio")
        os.makedirs(self.audio_dir, exist_ok=True)

    async def synthesize(self, text: str, language: str = "gu") -> Dict[str, Any]:
        from gtts import gTTS
        lang = language.lower()
        if lang not in ["gu", "hi", "en"]:
            lang = "gu"

        def _generate():
            tts = gTTS(text=text, lang=lang, slow=False)
            filename = f"tts_{lang}_{uuid.uuid4().hex[:8]}.mp3"
            filepath = os.path.join(self.audio_dir, filename)
            tts.save(filepath)
            with open(filepath, "rb") as f:
                content = f.read()
            return filename, content

        try:
            filename, content = await asyncio.to_thread(_generate)
            return {
                "audio_url": f"/uploads/audio/{filename}",
                "audio_content": content,
                "mime_type": "audio/mp3",
                "language": lang,
                "provider": "gTTS"
            }
        except Exception as e:
            logger.warning(f"gTTS audio synthesis failed: {e}. Falling back to mock TTS.")
            return await MockTextToSpeechProvider().synthesize(text, language)


class MockTextToSpeechProvider(TextToSpeechProvider):
    """Mock Text-to-Speech Provider providing reliable fallback without crashing."""

    async def synthesize(self, text: str, language: str = "gu") -> Dict[str, Any]:
        return {
            "audio_url": None,
            "audio_content": b"",
            "mime_type": "audio/mp3",
            "language": language,
            "provider": "mock_tts"
        }


def get_tts_provider() -> TextToSpeechProvider:
    provider = (settings.VOICE_TTS_PROVIDER or "gtts").lower()
    if provider in ["gtts", "google"]:
        return GTTSVoiceProvider()
    return MockTextToSpeechProvider()

tts_service = get_tts_provider()
