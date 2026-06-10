from __future__ import annotations

import base64
import json
import time

from google import genai
from google.genai.errors import APIError, ClientError, ServerError
from google.genai import types
from openai import OpenAI

from app.config import settings
from app.models.schema import BillExtraction
from app.services.file_service import SavedUpload
from app.services.preprocessing import preprocess_image
from app.services.sample_data_service import get_sample_bill
from app.services.validation_service import normalize_bill


PROMPT = """
You are extracting data from Indian electricity bills for an Excel automation workflow.

Return strict JSON with this top-level structure:
{
  "bills": [
    {
      "source_name": "...",
      "utility_name": "...",
      "consumer_name": "...",
      "consumer_number": "...",
      "address": "...",
      "mobile_number": "...",
      "meter_number": "...",
      "bill_month_label": "Jan",
      "bill_year": 2026,
      "bill_date": "2026-01-10",
      "due_date": "2026-01-30",
      "payable_amount": 1460.0,
      "payable_after_due": 1470.0,
      "fixed_charges": null,
      "excel_bill_amount": null,
      "sanctioned_load_kw": 3.3,
      "sanctioned_load_text": "3.30 KW",
      "connection_type": "90/LT I Res 1-Phase",
      "tariff_category": "90/LT I Res 1-Phase",
      "previous_reading": 33674,
      "current_reading": 33699,
      "units_consumed": 25,
      "monthly_history": [
        {"month_label": "Feb 2025", "month_iso": "2025-02", "units": 99, "confidence": 0.76}
      ],
      "confidence": {
        "consumer_name": 0.95,
        "consumer_number": 0.98
      },
      "raw_notes": ["Any ambiguity or explanation here"]
    }
  ]
}

Rules:
- Extract values exactly from the image when readable.
- If a value is unclear, set it to null and note the ambiguity in raw_notes.
- Include the 12-month history if visible.
- excel_bill_amount is the bill amount intended for the Excel sheet's unit-cost calculation. If the breakup is unclear, leave it null.
- Do not invent data.
- Return JSON only.
"""


class ExtractionError(RuntimeError):
    pass


def extract_bill(upload: SavedUpload) -> BillExtraction:
    sample = get_sample_bill(upload.original_path, upload.source_name)
    if sample is not None:
        return sample

    provider = resolve_provider()
    if provider == "gemini":
        extraction = extract_with_gemini(upload)
    elif provider == "openai":
        extraction = extract_with_openai(upload)
    else:
        raise ExtractionError("No supported AI provider is configured.")

    return normalize_bill(extraction)


def resolve_provider() -> str:
    if settings.ai_provider == "gemini":
        if not settings.gemini_api_key:
            raise ExtractionError("AI_PROVIDER is set to gemini, but GEMINI_API_KEY is missing.")
        return "gemini"

    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise ExtractionError("AI_PROVIDER is set to openai, but OPENAI_API_KEY is missing.")
        return "openai"

    if settings.gemini_api_key:
        return "gemini"
    if settings.openai_api_key:
        return "openai"
    raise ExtractionError("Configure GEMINI_API_KEY or OPENAI_API_KEY before extraction.")


def extract_with_gemini(upload: SavedUpload) -> BillExtraction:
    client = genai.Client(api_key=settings.gemini_api_key)
    contents: list[str | types.Part] = [PROMPT]

    for image_path in upload.image_paths:
        contents.append(
            types.Part.from_bytes(
                data=preprocess_image(image_path),
                mime_type="image/jpeg",
            )
        )

    models_to_try = [settings.gemini_model]
    models_to_try.extend(
        model for model in settings.gemini_fallback_models if model not in models_to_try
    )

    last_error: Exception | None = None

    for model_name in models_to_try:
        for attempt in range(1, settings.extraction_max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=0,
                        response_mime_type="application/json",
                    ),
                )

                payload = response.text or ""
                data = parse_json_payload(payload)
                bills = data.get("bills") or []
                if not bills:
                    raise ExtractionError(
                        f"Gemini model {model_name} returned no bill records."
                    )

                first_bill = dict(bills[0])
                first_bill["source_name"] = upload.source_name
                extraction = BillExtraction(**first_bill)
                extraction.raw_notes.append(f"Extracted with Gemini model: {model_name}")
                return extraction
            except (ServerError, APIError) as exc:
                last_error = exc
                if not is_retryable_gemini_error(exc):
                    break
                if attempt == settings.extraction_max_retries:
                    break
                time.sleep(settings.extraction_retry_delay_seconds * attempt)
            except (ClientError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                break
            except Exception as exc:  # pragma: no cover
                last_error = exc
                break

    raise ExtractionError(build_gemini_error_message(last_error))


def extract_with_openai(upload: SavedUpload) -> BillExtraction:
    client = OpenAI(api_key=settings.openai_api_key)
    content = [{"type": "text", "text": PROMPT}]

    for image_path in upload.image_paths:
        encoded = base64.b64encode(preprocess_image(image_path)).decode("utf-8")
        mime = "image/jpeg"
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{encoded}"},
            }
        )

    response = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0,
        messages=[{"role": "user", "content": content}],
    )

    payload = response.choices[0].message.content or ""
    data = parse_json_payload(payload)
    bills = data.get("bills") or []
    if not bills:
        raise ExtractionError("OpenAI response did not contain any bill records.")

    first_bill = dict(bills[0])
    first_bill["source_name"] = upload.source_name
    return BillExtraction(**first_bill)


def parse_json_payload(payload: str) -> dict:
    cleaned = payload.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
    if cleaned.startswith("json"):
        cleaned = cleaned[4:].strip()
    return json.loads(cleaned)


def is_retryable_gemini_error(exc: Exception) -> bool:
    text = str(exc).lower()
    status_code = getattr(exc, "status_code", None)
    code = getattr(exc, "code", None)
    return (
        status_code in {429, 500, 502, 503, 504}
        or code in {429, 500, 502, 503, 504}
        or "503" in text
        or "unavailable" in text
        or "overloaded" in text
        or "high demand" in text
        or "rate limit" in text
    )


def build_gemini_error_message(last_error: Exception | None) -> str:
    if last_error is None:
        return (
            "Gemini extraction failed. Please try again, switch to another Gemini model, "
            "or use a clearer bill image."
        )

    text = str(last_error)
    lowered = text.lower()
    if "503" in lowered or "unavailable" in lowered or "high demand" in lowered:
        return (
            "Gemini is temporarily overloaded for this bill image. The app already retried and "
            "tried fallback models. Please try again after a minute or use a clearer image."
        )
    if "429" in lowered or "rate limit" in lowered:
        return (
            "Gemini rate limit was reached. Wait a little and try again, or use a different API key."
        )
    if "json" in lowered:
        return (
            "The AI returned an unreadable extraction response. Please retry with a clearer bill image."
        )
    return f"Gemini extraction failed: {text}"
