from pathlib import Path

from app.models.subtitle import SubtitleSegment, SubtitleStyle
from app.services.subtitle_service import parse_srt_text, subtitles_to_ass_file, subtitles_to_srt


def test_parse_srt_text_round_trip() -> None:
    srt_text = """1
00:00:01,000 --> 00:00:03,500
Hello world

2
00:00:04,000 --> 00:00:05,250
Second line
"""

    subtitles = parse_srt_text(srt_text)

    assert len(subtitles) == 2
    assert subtitles[0].id == "1"
    assert subtitles[0].start_time == 1.0
    assert subtitles[0].end_time == 3.5
    assert subtitles[0].text == "Hello world"


def test_subtitles_to_srt_and_ass_file(tmp_path: Path) -> None:
    subtitles = [
        SubtitleSegment(id="1", start_time=1.0, end_time=2.0, text="Hello"),
        SubtitleSegment(id="2", start_time=2.5, end_time=4.0, text="World"),
    ]
    styles = SubtitleStyle(
        font_family="Arial",
        font_size=42,
        text_color="#FFFFFF",
        background_color="#000000",
        bg_opacity=0.5,
    )

    srt_text = subtitles_to_srt(subtitles)
    ass_path = subtitles_to_ass_file(subtitles, styles, tmp_path / "captions.ass")

    assert "00:00:01,000 --> 00:00:02,000" in srt_text
    assert ass_path.exists()