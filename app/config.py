from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    ai_provider: str = os.getenv("AI_PROVIDER", "auto").lower()
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    app_env: str = os.getenv("APP_ENV", "development")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    template_path: Path = BASE_DIR / os.getenv("TEMPLATE_PATH", "assets/template.xlsx")
    output_dir: Path = BASE_DIR / os.getenv("OUTPUT_DIR", "generated")
    temp_dir: Path = BASE_DIR / os.getenv("TEMP_DIR", "tmp")
    max_upload_bills: int = int(os.getenv("MAX_UPLOAD_BILLS", "5"))


settings = Settings()
settings.output_dir.mkdir(parents=True, exist_ok=True)
settings.temp_dir.mkdir(parents=True, exist_ok=True)
