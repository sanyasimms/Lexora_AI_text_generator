from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.export_video import router as export_video_router
from app.api.routes.transcribe_translate import router as transcribe_translate_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.utils.temp_paths import ensure_temp_dir

configure_logging()
settings = get_settings()
ensure_temp_dir()

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_translate_router, prefix=settings.api_v1_prefix)
app.include_router(export_video_router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": settings.project_name}
