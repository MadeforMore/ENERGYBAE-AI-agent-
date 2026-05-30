# Energybae Bill-to-Excel Automation

A practical internship submission that reads an electricity bill, extracts the key values with AI, lets the user review the result, and fills the provided Excel template without overwriting formulas.

## What this project does

- Upload up to five electricity bills as `PDF`, `JPG`, `JPEG`, or `PNG`
- Convert PDF pages to images and improve them for OCR / vision extraction
- Extract bill fields with an OpenAI vision model
- Show extracted values with confidence scores and validation warnings
- Let the user edit uncertain values before export
- Fill the provided Excel template while preserving all workbook formulas
- Return a ready-to-download `.xlsx` output

## Recommended stack

- `FastAPI`: simple backend, async-friendly, easy to demo
- `Jinja2 + vanilla JS`: fast delivery without a frontend build step
- `Gemini API or OpenAI vision model`: both support multimodal extraction
- `PyMuPDF + Pillow + OpenCV`: robust PDF/image preprocessing
- `openpyxl`: safest path to preserve formulas while writing only input cells

## Why this stack

- It is fast to build and explain in an interview.
- It supports scanned bills, PDFs, and mobile photos with one pipeline.
- It keeps the Excel template intact instead of rebuilding calculations in code.
- It stays production-friendly because extraction, validation, and Excel writing are cleanly separated.

## Alternatives considered

- `Streamlit`: faster UI, but weaker separation between product layers
- `React + FastAPI`: stronger frontend experience, but slower to finish for an internship task
- `Azure Document Intelligence / Google Document AI`: excellent OCR, but extra setup and vendor complexity
- `Tesseract-only OCR`: cheaper, but less reliable on noisy Marathi/English bill photos

## Project structure

```text
app/
  api/
  models/
  services/
  static/
  templates/
assets/
  samples/
  template.xlsx
docs/
tests/
```

## Setup

1. Create a virtual environment.
2. Install dependencies.
3. Add your Gemini or OpenAI API key.
4. Start the FastAPI app.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Environment variables

See `.env.example`.

- `AI_PROVIDER`: `auto`, `gemini`, or `openai`
- `GEMINI_API_KEY`: recommended if you want to use Google's free tier
- `GEMINI_MODEL`: defaults to `gemini-2.5-flash`
- `OPENAI_API_KEY`: required for AI extraction
- `OPENAI_MODEL`: defaults to `gpt-4o`
- `TEMPLATE_PATH`: defaults to `assets/template.xlsx`
- `OUTPUT_DIR`: where generated workbooks are saved
- `MAX_UPLOAD_BILLS`: defaults to `2`

If `AI_PROVIDER=auto`, the app prefers Gemini when `GEMINI_API_KEY` is present, otherwise it falls back to OpenAI.

For the two exact sample bill images included in `assets/samples/`, the app can also extract data locally without any API key. This is useful for demoing the internship submission immediately.

## Workflow

1. Upload one to five bills
2. Preview uploaded bill images
3. Click `Extract Data`
4. Review or edit extracted fields
5. Click `Generate Excel`
6. Download the filled workbook, or a ZIP of multiple workbooks when more than two bills are uploaded

## System flow

```text
User Upload
   |
   v
File Validation
   |
   v
PDF/Image Normalization
   |
   v
OpenAI Vision Extraction
   |
   v
Schema Validation + Business Checks
   |
   v
User Review / Edit
   |
   v
Excel Template Fill
   |
   v
Download Completed Workbook
```

## Validation rules

- Consumer and meter identifiers are normalized to digit strings
- Current reading minus previous reading is checked against units consumed
- Missing `excel_bill_amount` falls back to visible payable amount
- Missing `fixed_charges` is flagged for review
- Monthly history is normalized to a 12-month window ending at the bill month
- Formula cells are preserved and their cached values are also written so the output shows calculated values immediately

## Formula safety

This project never rewrites formula cells. It only edits workbook input cells identified during analysis of the provided template. See [docs/analysis.md](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/docs/analysis.md).

## Testing

```powershell
pytest
```

## Deployment

### Local demo

- Run with `uvicorn`
- Store generated files in `generated/`

### Production

- Containerize with Docker
- Deploy on Azure App Service, Render, Railway, or ECS
- Store uploaded files in object storage
- Move generated workbooks to short-lived temp storage
- Add auth and request logging

## Future improvements

- Add a second extraction provider fallback
- Support more bill layouts beyond MSEDCL
- Add human-in-the-loop approval queues
- Persist extraction feedback for continuous prompt improvement
- Add workbook template versioning
