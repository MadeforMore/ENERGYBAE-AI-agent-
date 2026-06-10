from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def is_vercel_runtime() -> bool:
    return bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))


def resolve_repo_path(raw_value: str, default_value: str) -> Path:
    value = raw_value or default_value
    path = Path(value)
    return path if path.is_absolute() else BASE_DIR / path


def resolve_writable_runtime_path(raw_value: str, default_value: str) -> Path:
    value = raw_value or default_value
    path = Path(value)
    if path.is_absolute():
        return path
    if is_vercel_runtime():
        return Path("/tmp") / path
    return BASE_DIR / path


@dataclass(frozen=True)
class Settings:
    ai_provider: str = os.getenv("AI_PROVIDER", "auto").lower()
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    gemini_fallback_models: tuple[str, ...] = tuple(
        model.strip()
        for model in os.getenv("GEMINI_FALLBACK_MODELS", "gemini-2.5-flash-lite,gemini-2.0-flash").split(",")
        if model.strip()
    )
    extraction_max_retries: int = int(os.getenv("EXTRACTION_MAX_RETRIES", "3"))
    extraction_retry_delay_seconds: float = float(os.getenv("EXTRACTION_RETRY_DELAY_SECONDS", "2"))
    app_env: str = os.getenv("APP_ENV", "development")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    is_vercel: bool = field(default_factory=is_vercel_runtime)
    template_path: Path = field(
        default_factory=lambda: resolve_repo_path(
            os.getenv("TEMPLATE_PATH", ""),
            "assets/template.xlsx",
        )
    )
    output_dir: Path = field(
        default_factory=lambda: resolve_writable_runtime_path(
            os.getenv("OUTPUT_DIR", ""),
            "generated",
        )
    )
    temp_dir: Path = field(
        default_factory=lambda: resolve_writable_runtime_path(
            os.getenv("TEMP_DIR", ""),
            "tmp",
        )
    )
    max_upload_bills: int = int(os.getenv("MAX_UPLOAD_BILLS", "5"))


settings = Settings()
settings.output_dir.mkdir(parents=True, exist_ok=True)
settings.temp_dir.mkdir(parents=True, exist_ok=True)
