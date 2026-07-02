from functools import lru_cache
from shutil import which
from pathlib import Path

import imageio_ffmpeg
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = "AI Video Caption Translator & Stylist"
    api_v1_prefix: str = "/api"
    openai_api_key: str = ""
    ffmpeg_path: str = "ffmpeg"
    temp_dir: Path = Path("./tmp")
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def ffmpeg_executable(self) -> str:
        configured_path = self.ffmpeg_path.strip()
        if configured_path and which(configured_path):
            return configured_path

        bundled_path = imageio_ffmpeg.get_ffmpeg_exe()
        if bundled_path:
            return bundled_path

        raise RuntimeError("FFmpeg executable could not be resolved")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
