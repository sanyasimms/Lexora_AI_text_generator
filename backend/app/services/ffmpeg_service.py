from __future__ import annotations

import asyncio
from pathlib import Path

from app.core.config import get_settings


def _ffmpeg_subtitles_filter_path(path: Path) -> str:
    resolved_path = path.resolve().as_posix().replace(":", r"\:")
    return f"subtitles='{resolved_path}'"


async def extract_audio_to_mp3(video_path: Path, audio_path: Path) -> Path:
    settings = get_settings()
    process = await asyncio.create_subprocess_exec(
        settings.ffmpeg_executable,
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "libmp3lame",
        str(audio_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(stderr.decode() or stdout.decode() or "Audio extraction failed")
    return audio_path


async def burn_subtitles_to_video(video_path: Path, ass_path: Path, output_path: Path) -> Path:
    settings = get_settings()
    process = await asyncio.create_subprocess_exec(
        settings.ffmpeg_executable,
        "-y",
        "-i",
        str(video_path),
        "-vf",
        _ffmpeg_subtitles_filter_path(ass_path),
        "-c:a",
        "copy",
        str(output_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(stderr.decode() or stdout.decode() or "Video export failed")
    return output_path
