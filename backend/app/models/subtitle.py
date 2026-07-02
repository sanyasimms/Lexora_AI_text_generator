from pydantic import BaseModel, Field


class SubtitleSegment(BaseModel):
    id: str = Field(..., description="Stable subtitle segment identifier")
    start_time: float = Field(..., ge=0)
    end_time: float = Field(..., ge=0)
    text: str = Field(..., min_length=1)


class SubtitleStyle(BaseModel):
    font_family: str = Field(default="Arial")
    font_size: int = Field(default=42, ge=8, le=128)
    text_color: str = Field(default="#FFFFFF")
    background_color: str = Field(default="#000000")
    bg_opacity: float = Field(default=0.5, ge=0.0, le=1.0)


class SubtitlePayload(BaseModel):
    source_language: str
    target_language: str
    subtitles: list[SubtitleSegment]
