from contextlib import suppress
from pathlib import Path


def safe_unlink(path: Path | None) -> None:
    if not path:
        return
    with suppress(FileNotFoundError):
        path.unlink()
