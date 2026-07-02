# Backend

FastAPI backend for the AI Video Caption Translator & Stylist application.

## What It Does

- Accepts uploaded video files
- Extracts audio to temporary MP3 files with FFmpeg
- Detects spoken language with Whisper
- Produces timestamped subtitles in SRT format
- Translates subtitle text with GPT-4o-mini while preserving timestamps
- Exports styled caption videos by burning `.ass` subtitles into the source video

## Install

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Environment

Copy `.env.example` to `.env` and set:

```env
OPENAI_API_KEY=your_openai_key
FFMPEG_PATH=ffmpeg
TEMP_DIR=./tmp
CORS_ORIGINS=http://localhost:3000
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` - service name
- `GET /health` - health check
- `POST /api/transcribe-translate` - upload a video and get translated subtitle segments
- `POST /api/export-video` - upload a video, subtitles, and styles to get a rendered output video

## Notes

- Temporary files are written to `TEMP_DIR` and cleaned up after processing.
- FFmpeg must be installed and available on your system path unless `FFMPEG_PATH` points to a different executable.