import json
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import export_video as export_video_route
from app.api.routes import transcribe_translate as transcribe_translate_route


client = TestClient(app)


def test_export_video_rejects_invalid_payload() -> None:
    response = client.post(
        "/api/export-video",
        files={"video_file": ("sample.mp4", BytesIO(b"fake-video"), "video/mp4")},
        data={"subtitles": "not-json", "styles": "also-not-json"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid subtitles or styles payload"


def test_transcribe_translate_happy_path(monkeypatch) -> None:
    class DummyWhisperService:
        def transcribe_to_srt(self, audio_path: Path) -> tuple[str, str]:
            return (
                "1\n00:00:01,000 --> 00:00:02,000\nHello world\n",
                "en",
            )

    class DummyTranslationService:
        def translate_srt(self, srt_text: str, target_language: str) -> str:
            assert target_language == "es"
            return "1\n00:00:01,000 --> 00:00:02,000\nHola mundo\n"

    async def fake_extract_audio_to_mp3(video_path: Path, audio_path: Path) -> Path:
        audio_path.write_bytes(b"audio")
        return audio_path

    monkeypatch.setattr(transcribe_translate_route, "WhisperService", DummyWhisperService)
    monkeypatch.setattr(transcribe_translate_route, "TranslationService", DummyTranslationService)
    monkeypatch.setattr(transcribe_translate_route, "extract_audio_to_mp3", fake_extract_audio_to_mp3)

    response = client.post(
        "/api/transcribe-translate",
        files={"video_file": ("sample.mp4", BytesIO(b"fake-video"), "video/mp4")},
        data={"target_language": "es"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["source_language"] == "en"
    assert payload["target_language"] == "es"
    assert payload["subtitles"][0]["text"] == "Hola mundo"


def test_export_video_happy_path(monkeypatch, tmp_path) -> None:
    async def fake_burn_subtitles_to_video(video_path: Path, ass_path: Path, output_path: Path) -> Path:
        output_path.write_bytes(b"rendered-video")
        return output_path

    monkeypatch.setattr(export_video_route, "burn_subtitles_to_video", fake_burn_subtitles_to_video)
    monkeypatch.setattr(export_video_route, "make_temp_file_path", lambda prefix, suffix: tmp_path / f"{prefix}{suffix}")

    response = client.post(
        "/api/export-video",
        files={"video_file": ("sample.mp4", BytesIO(b"fake-video"), "video/mp4")},
        data={
            "subtitles": json.dumps([
                {"id": "1", "start_time": 1.0, "end_time": 2.0, "text": "Hello"}
            ]),
            "styles": json.dumps(
                {
                    "font_family": "Arial",
                    "font_size": 42,
                    "text_color": "#FFFFFF",
                    "background_color": "#000000",
                    "bg_opacity": 0.5,
                }
            ),
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    assert response.content == b"rendered-video"