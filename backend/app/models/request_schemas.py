from pydantic import BaseModel, Field

from app.models.subtitle import SubtitleSegment, SubtitleStyle


class TranscribeTranslateResponse(BaseModel):
    source_language: str
    target_language: str
    subtitles: list[SubtitleSegment]


class ExportVideoResponse(BaseModel):
    detail: str = "Video export started"
    output_filename: str | None = None


class SubtitleEditRequest(BaseModel):
    subtitles: list[SubtitleSegment]
    styles: SubtitleStyle
    target_language: str = Field(default="en")
