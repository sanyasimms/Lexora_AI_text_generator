from __future__ import annotations

import re
from pathlib import Path

import pysubs2

from app.models.subtitle import SubtitleSegment, SubtitleStyle


_SRT_TIME_PATTERN = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})"
)


def _timecode_to_seconds(value: str) -> float:
    hours, minutes, rest = value.replace(",", ".").split(":")
    seconds, milliseconds = rest.split(".")
    return (int(hours) * 3600) + (int(minutes) * 60) + int(seconds) + (int(milliseconds) / 1000)


def parse_srt_text(srt_text: str) -> list[SubtitleSegment]:
    blocks: list[SubtitleSegment] = []
    raw_blocks = [block.strip() for block in srt_text.strip().split("\n\n") if block.strip()]

    for raw_block in raw_blocks:
        lines = [line.strip() for line in raw_block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue

        index = lines[0]
        match = _SRT_TIME_PATTERN.search(lines[1])
        if not match:
            continue

        text = " ".join(lines[2:]).strip()
        blocks.append(
            SubtitleSegment(
                id=index,
                start_time=_timecode_to_seconds(match.group("start")),
                end_time=_timecode_to_seconds(match.group("end")),
                text=text,
            )
        )

    return blocks


def subtitles_to_srt(subtitles: list[SubtitleSegment]) -> str:
    entries: list[str] = []
    for position, subtitle in enumerate(subtitles, start=1):
        entries.append(
            "\n".join(
                [
                    str(position),
                    f"{_seconds_to_srt_time(subtitle.start_time)} --> {_seconds_to_srt_time(subtitle.end_time)}",
                    subtitle.text,
                ]
            )
        )
    return "\n\n".join(entries)


def _seconds_to_srt_time(total_seconds: float) -> str:
    milliseconds_total = int(round(total_seconds * 1000))
    hours, remainder = divmod(milliseconds_total, 3600 * 1000)
    minutes, remainder = divmod(remainder, 60 * 1000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def _hex_to_color(value: str, opacity: float = 1.0) -> pysubs2.Color:
    normalized = value.strip().lstrip("#")
    if len(normalized) != 6:
        raise ValueError(f"Invalid hex color: {value}")

    red = int(normalized[0:2], 16)
    green = int(normalized[2:4], 16)
    blue = int(normalized[4:6], 16)
    alpha = int(round((1 - opacity) * 255))
    return pysubs2.Color(red, green, blue, alpha)


def subtitles_to_ass_file(subtitles: list[SubtitleSegment], styles: SubtitleStyle, output_path: Path) -> Path:
    subs = pysubs2.SSAFile()
    subs.info["PlayResX"] = "1920"
    subs.info["PlayResY"] = "1080"
    subs.styles["Default"] = pysubs2.SSAStyle(
        fontname=styles.font_family,
        fontsize=styles.font_size,
        primarycolor=_hex_to_color(styles.text_color),
        backcolor=_hex_to_color(styles.background_color, styles.bg_opacity),
        outline=2,
        shadow=0,
        marginl=50,
        marginr=50,
        marginv=60,
        bold=False,
        italic=False,
        underline=False,
        strikeout=False,
        scalex=100,
        scaley=100,
        spacing=0,
        angle=0,
        borderstyle=3,
        outlinecolor=_hex_to_color(styles.background_color, styles.bg_opacity),
        alignment=pysubs2.Alignment.BOTTOM_CENTER,
    )

    for subtitle in subtitles:
        subs.events.append(
            pysubs2.SSAEvent(
                start=int(subtitle.start_time * 1000),
                end=int(subtitle.end_time * 1000),
                text=subtitle.text,
                style="Default",
            )
        )

    subs.save(str(output_path))
    return output_path
