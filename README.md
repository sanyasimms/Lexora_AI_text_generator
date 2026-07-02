# AI Video Caption Translator & Stylist

A full-stack web application for uploading videos, detecting spoken language, transcribing with timestamps, translating captions with AI, styling subtitles with live preview, and exporting a finished burn-in video through FFmpeg.

## Overview

This application combines a modern Next.js frontend with a FastAPI backend to provide an end-to-end subtitle translation and styling workflow.

Users can:

- Upload a video file
- Detect spoken language automatically
- Transcribe audio into timestamped subtitles
- Translate captions into a target language using AI
- Edit subtitles manually before export
- Customize fonts, colors, and background styling with live preview
- Export a final hard-burned caption video using FFmpeg

## Tech Stack

### Frontend
- Next.js 14+ App Router
- JavaScript
- Tailwind CSS
- React state for playback, subtitle timing, and styles
- HTML5 video playback with subtitle overlay

### Backend
- Python
- FastAPI
- OpenAI Whisper API for transcription
- GPT-4o-mini for subtitle translation
- `pysubs2` for `.ass` subtitle generation
- FFmpeg for audio extraction and final video burn-in

## Core Features

### 1. Video Upload and Analysis
- Accepts uploaded video files from the browser
- Extracts audio server-side
- Sends audio to Whisper for timestamped transcription
- Detects spoken language and returns structured subtitle segments

### 2. AI Translation
- Sends raw subtitle text to GPT-4o-mini
- Uses strict prompting to preserve timestamps exactly
- Returns translated subtitle segments as JSON

### 3. Live Styling Preview
- Renders subtitles over the video player in real time
- Supports font, font size, text color, background color, and opacity
- Updates preview instantly as the user edits styles

### 4. Subtitle Editing
- Displays a timeline-style subtitle editor
- Allows text correction before export
- Keeps subtitle timing intact unless manually adjusted

### 5. Video Export
- Builds an `.ass` file using `pysubs2`
- Injects user styling into subtitle rendering
- Runs FFmpeg to burn subtitles into the output video
- Returns the processed video for download

## Suggested Folder Structure

```bash
ai-video-caption-translator-stylist/
├─ frontend/
│  ├─ app/
│  │  ├─ page.jsx
│  │  ├─ layout.jsx
│  │  └─ globals.css
│  ├─ components/
│  │  ├─ VideoPlayer.jsx
│  │  ├─ StylePanel.jsx
│  │  ├─ SubtitleEditor.jsx
│  │  └─ UploadDropzone.jsx
│  ├─ lib/
│  │  ├─ api.js
│  │  ├─ subtitleUtils.js
│  │  └─ constants.js
│  ├─ hooks/
│  │  ├─ useVideoTime.js
│  │  └─ useSubtitleStyles.js
│  ├─ tailwind.config.js
│  ├─ postcss.config.js
│  └─ jsconfig.json
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  └─ logging.py
│  │  ├─ api/
│  │  │  └─ routes/
│  │  │     ├─ transcribe_translate.py
│  │  │     └─ export_video.py
│  │  ├─ services/
│  │  │  ├─ ffmpeg_service.py
│  │  │  ├─ whisper_service.py
│  │  │  ├─ translation_service.py
│  │  │  └─ subtitle_service.py
│  │  ├─ models/
│  │  │  ├─ subtitle.py
│  │  │  └─ request_schemas.py
│  │  └─ utils/
│  │     ├─ file_cleanup.py
│  │     └─ temp_paths.py
│  ├─ requirements.txt
│  └─ .env.example
├─ shared/
│  └─ types/
│     └─ subtitle.schema.json
├─ README.md
└─ docker-compose.yml
```

## Frontend Architecture

### State Model

The frontend should maintain these core state objects:

```js
subtitles: [
  {
    id: string,
    startTime: number,
    endTime: number,
    text: string,
  }
]

styles: {
  fontFamily: string,
  fontSize: number,
  textColor: string,
  backgroundColor: string,
  bgOpacity: number,
}

currentPlaybackTime: number
```

### Key Components

#### `VideoPlayer.jsx`
- Renders the uploaded video
- Syncs playback time with subtitle rendering
- Overlays a subtitle preview box above the video
- Highlights the active subtitle segment based on `currentPlaybackTime`

#### `StylePanel.jsx`
- Lets users choose font family
- Includes font size slider
- Includes text and background color pickers
- Includes background opacity control
- Includes target language selector

#### `SubtitleEditor.jsx`
- Lists subtitle segments in timeline order
- Allows text correction before export
- Supports editing timestamps if needed
- Shows a clean, export-ready subtitle table

### Frontend Data Flow

1. User uploads a video
2. Frontend sends file to backend transcription endpoint
3. Backend returns timestamped subtitle JSON
4. Frontend stores subtitle data in state
5. User edits text and style settings
6. Preview updates live in `VideoPlayer`
7. User exports final video through backend

## Backend Architecture

### Endpoint 1: `POST /api/transcribe-translate`

#### Responsibilities
- Accept uploaded video file
- Extract audio to temporary `.mp3`
- Send audio to Whisper with `response_format="srt"`
- Send raw SRT to GPT-4o-mini
- Preserve timestamps exactly
- Return translated subtitle segments as JSON

#### Expected Response Shape
```json
{
  "source_language": "en",
  "target_language": "es",
  "subtitles": [
    {
      "id": "1",
      "startTime": 0,
      "endTime": 2.4,
      "text": "Hola, bienvenidos."
    }
  ]
}
```

### Endpoint 2: `POST /api/export-video`

#### Responsibilities
- Accept original video file
- Accept edited subtitles JSON
- Accept style configuration
- Build `.ass` subtitle file using `pysubs2`
- Burn subtitles into video using FFmpeg
- Return downloadable processed video

#### Export Flow
1. Save uploaded video to temporary storage
2. Generate `.ass` caption file
3. Run FFmpeg subtitle burn-in
4. Stream final video back to client
5. Clean up all temporary files

## Operational Design Principles

### File Cleanup
- Remove temporary uploaded files after each request
- Delete extracted audio after transcription completes
- Remove generated `.ass` files after export
- Use `try/finally` cleanup blocks for safety

### Type Safety
- Share subtitle and style schemas between frontend and backend
- Validate request payloads with Pydantic
- Type frontend API responses with JSDoc comments or shared JSON schema

### Performance
- Use async FastAPI endpoints
- Offload FFmpeg work to background-safe execution
- Keep frontend video preview lightweight
- Avoid unnecessary re-renders by isolating state updates

## Environment Variables

### Frontend
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Backend
```env
OPENAI_API_KEY=your_openai_key
FFMPEG_PATH=ffmpeg
TEMP_DIR=./tmp
```

## Planned Execution Flow

1. Upload video from the frontend
2. Transcribe and detect language in FastAPI
3. Translate subtitle text while preserving timestamps
4. Render subtitle timeline for user review
5. Apply live styling in the preview player
6. Export final video with embedded captions

## Notes

This README describes the intended architecture and structure only. No implementation files have been started yet.

If you want, I can next turn this into the actual project scaffold and core implementation files using JavaScript for the frontend.