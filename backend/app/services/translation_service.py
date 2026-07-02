from __future__ import annotations

from openai import OpenAI

from app.core.config import get_settings


class TranslationService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)

    def translate_srt(self, srt_text: str, target_language: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You translate subtitle SRT content into the target language. "
                        "Keep the numeric indices and timestamps exactly unchanged. "
                        "Only translate the subtitle text lines. Return only valid SRT and no commentary."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Target language: {target_language}\n\nSRT:\n{srt_text}",
                },
            ],
            temperature=0,
        )
        translated_text = response.choices[0].message.content or ""
        if not translated_text.strip():
            raise ValueError("Translation service returned empty SRT content")
        return translated_text
