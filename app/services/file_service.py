from __future__ import annotations

import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

import fitz
from fastapi import UploadFile

from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


@dataclass
class SavedUpload:
    source_name: str
    original_path: Path
    image_paths: list[Path]


def ensure_allowed_file(filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")


async def save_upload(upload: UploadFile) -> SavedUpload:
    ensure_allowed_file(upload.filename or "upload")
    job_dir = settings.temp_dir / f"upload_{uuid.uuid4().hex}"
    job_dir.mkdir(parents=True, exist_ok=True)

    original_path = job_dir / (upload.filename or "uploaded_file")
    with original_path.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    image_paths = convert_to_images(original_path, job_dir)
    return SavedUpload(
        source_name=upload.filename or original_path.name,
        original_path=original_path,
        image_paths=image_paths,
    )


def convert_to_images(source_path: Path, output_dir: Path) -> list[Path]:
    if source_path.suffix.lower() != ".pdf":
        return [source_path]

    document = fitz.open(source_path)
    page_paths: list[Path] = []
    for page_index in range(document.page_count):
        page = document.load_page(page_index)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
        page_path = output_dir / f"{source_path.stem}_page_{page_index + 1}.jpg"
        pixmap.save(page_path)
        page_paths.append(page_path)
    document.close()
    return page_paths
