from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models.schema import ExtractResponse, ExtractionFailure, GenerateWorkbookRequest
from app.services.excel_service import build_workbooks
from app.services.extraction_service import ExtractionError, extract_bill
from app.services.file_service import save_upload


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "max_upload_bills": settings.max_upload_bills,
            "ai_provider": settings.ai_provider,
            "gemini_configured": bool(settings.gemini_api_key),
            "openai_configured": bool(settings.openai_api_key),
        },
    )


@router.post("/api/extract", response_model=ExtractResponse)
async def extract(files: list[UploadFile] = File(...)) -> ExtractResponse:
    if not files:
        raise HTTPException(status_code=400, detail="At least one file is required.")
    if len(files) > settings.max_upload_bills:
        raise HTTPException(
            status_code=400,
            detail=f"Only {settings.max_upload_bills} bill files are supported by this template.",
        )

    bills = []
    errors: list[ExtractionFailure] = []
    assumptions: list[str] = []

    for upload in files:
        try:
            saved = await save_upload(upload)
            bills.append(extract_bill(saved))
        except ValueError as exc:
            errors.append(ExtractionFailure(source_name=upload.filename or "upload", message=str(exc)))
        except ExtractionError as exc:
            errors.append(ExtractionFailure(source_name=upload.filename or "upload", message=str(exc)))
        except Exception as exc:  # pragma: no cover
            errors.append(
                ExtractionFailure(
                    source_name=upload.filename or "upload",
                    message=f"Failed to process file: {exc}",
                )
            )

    assumptions.append(
        "If the Excel-specific bill amount is not found, the visible payable amount is used as a fallback."
    )
    assumptions.append(
        "When one bill is uploaded, the left template section is filled and the right section is cleared."
    )
    assumptions.append(
        "If AI_PROVIDER is set to auto, Gemini is used first when a GEMINI_API_KEY is available."
    )
    assumptions.append(
        "The exact provided sample bill images can be extracted locally even without an API key."
    )
    assumptions.append(
        "For new bill images, the app retries Gemini automatically and tries fallback Gemini models when the service is busy."
    )
    if not bills and errors:
        assumptions.append(
            "No bill was extracted successfully. Review the error messages below and try again."
        )
    return ExtractResponse(bills=bills, assumptions=assumptions, errors=errors)


@router.post("/api/generate")
async def generate(request: GenerateWorkbookRequest) -> FileResponse:
    if not request.bills:
        raise HTTPException(status_code=400, detail="No bill data was supplied.")

    output_path = build_workbooks(request.bills, request.panel_wattage)
    media_type = (
        "application/zip"
        if output_path.suffix.lower() == ".zip"
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type=media_type,
    )


@router.get("/api/template-analysis")
async def template_analysis() -> dict[str, str]:
    return {
        "sheet": "Pranay HOME",
        "template_path": str(settings.template_path),
        "analysis_doc": str(Path("docs/analysis.md")),
    }


@router.get("/api/provider-status")
async def provider_status() -> dict[str, bool | str]:
    return {
        "ai_provider": settings.ai_provider,
        "gemini_configured": bool(settings.gemini_api_key),
        "openai_configured": bool(settings.openai_api_key),
        "sample_fallback_available": True,
    }
