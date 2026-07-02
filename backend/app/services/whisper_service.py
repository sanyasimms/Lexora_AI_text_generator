from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from app.core.config import get_settings


class WhisperService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)

    def transcribe_to_srt(self, audio_path: Path) -> tuple[str, str]:
        with audio_path.open("rb") as audio_file:
            detection_response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
            )

        with audio_path.open("rb") as audio_file:
            srt_response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="srt",
            )

        source_language = getattr(detection_response, "language", "unknown")
        return str(srt_response), source_language
