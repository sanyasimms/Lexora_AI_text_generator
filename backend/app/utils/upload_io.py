from __future__ import annotations

from pathlib import Path

from fastapi import UploadFile


async def save_upload_file(upload_file: UploadFile, destination: Path, chunk_size: int = 1024 * 1024) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as output_file:
        while True:
            chunk = await upload_file.read(chunk_size)
            if not chunk:
                break
            output_file.write(chunk)
    await upload_file.close()
    return destination