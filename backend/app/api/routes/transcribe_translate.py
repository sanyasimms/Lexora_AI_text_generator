from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.request_schemas import TranscribeTranslateResponse
from app.services.ffmpeg_service import extract_audio_to_mp3
from app.services.subtitle_service import parse_srt_text
from app.services.translation_service import TranslationService
from app.services.whisper_service import WhisperService
from app.utils.file_cleanup import safe_unlink
from app.utils.temp_paths import make_temp_file_path
from app.utils.upload_io import save_upload_file

router = APIRouter(tags=["transcribe-translate"])


@router.post("/transcribe-translate", response_model=TranscribeTranslateResponse)
async def transcribe_translate(
    video_file: UploadFile = File(...),
    target_language: str = Form("en"),
) -> TranscribeTranslateResponse:
    target_language = target_language.strip()
    if not target_language:
        raise HTTPException(status_code=400, detail="target_language is required")

    if not video_file.filename:
        raise HTTPException(status_code=400, detail="A video file is required")

    if video_file.content_type not in {"video/mp4", "video/quicktime", "video/x-matroska", "video/webm"}:
        raise HTTPException(status_code=400, detail="Unsupported video format")

    video_path = make_temp_file_path("upload", Path(video_file.filename or "video").suffix or ".mp4")
    audio_path = make_temp_file_path("audio", ".mp3")

    whisper_service = WhisperService()
    translation_service = TranslationService()

    try:
        await save_upload_file(video_file, video_path)
        await extract_audio_to_mp3(video_path, audio_path)

        srt_text, source_language = whisper_service.transcribe_to_srt(audio_path)
        translated_srt = translation_service.translate_srt(srt_text, target_language)
        subtitles = parse_srt_text(translated_srt)

        return TranscribeTranslateResponse(
            source_language=source_language,
            target_language=target_language,
            subtitles=subtitles,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        safe_unlink(video_path)
        safe_unlink(audio_path)
