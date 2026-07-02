import uuid
from pathlib import Path

from app.core.config import get_settings


def ensure_temp_dir() -> Path:
    settings = get_settings()
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    return settings.temp_dir


def make_temp_file_path(prefix: str, suffix: str) -> Path:
    temp_dir = ensure_temp_dir()
    return temp_dir / f"{prefix}_{uuid.uuid4().hex}{suffix}"
