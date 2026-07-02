from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.models.subtitle import SubtitleSegment, SubtitleStyle
from app.services.ffmpeg_service import burn_subtitles_to_video
from app.services.subtitle_service import subtitles_to_ass_file
from app.utils.file_cleanup import safe_unlink
from app.utils.temp_paths import make_temp_file_path
from app.utils.upload_io import save_upload_file

router = APIRouter(tags=["export-video"])


@router.post("/export-video")
async def export_video(
    background_tasks: BackgroundTasks,
    video_file: UploadFile = File(...),
    subtitles: str = Form(...),
    styles: str = Form(...),
) -> FileResponse:
    if not video_file.filename:
        raise HTTPException(status_code=400, detail="A video file is required")

    if video_file.content_type not in {"video/mp4", "video/quicktime", "video/x-matroska", "video/webm"}:
        raise HTTPException(status_code=400, detail="Unsupported video format")

    video_path = make_temp_file_path("source_video", Path(video_file.filename or "video").suffix or ".mp4")
    ass_path = make_temp_file_path("styled_captions", ".ass")
    output_path = make_temp_file_path("exported_video", ".mp4")

    try:
        try:
            subtitles_payload = [SubtitleSegment.model_validate(item) for item in json.loads(subtitles)]
            styles_payload = SubtitleStyle.model_validate(json.loads(styles))
        except (json.JSONDecodeError, TypeError, ValidationError, ValueError) as exc:
            raise HTTPException(status_code=400, detail="Invalid subtitles or styles payload") from exc

        await save_upload_file(video_file, video_path)
        subtitles_to_ass_file(subtitles_payload, styles_payload, ass_path)
        await burn_subtitles_to_video(video_path, ass_path, output_path)

        background_tasks.add_task(safe_unlink, video_path)
        background_tasks.add_task(safe_unlink, ass_path)
        background_tasks.add_task(safe_unlink, output_path)

        return FileResponse(
            path=str(output_path),
            filename=f"{video_path.stem}_captioned.mp4",
            media_type="video/mp4",
            background=background_tasks,
        )
    except HTTPException:
        safe_unlink(video_path)
        safe_unlink(ass_path)
        safe_unlink(output_path)
        raise
    except Exception as exc:
        safe_unlink(video_path)
        safe_unlink(ass_path)
        safe_unlink(output_path)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
