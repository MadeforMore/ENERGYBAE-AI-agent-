from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MonthlyUsage(BaseModel):
    month_label: str = ""
    month_iso: str | None = None
    units: float | None = None
    confidence: float = 0.0


class ValidationIssue(BaseModel):
    field: str
    message: str
    severity: str = "warning"


class BillExtraction(BaseModel):
    source_name: str
    utility_name: str | None = None
    consumer_name: str | None = None
    consumer_number: str | None = None
    address: str | None = None
    mobile_number: str | None = None
    meter_number: str | None = None
    bill_month_label: str | None = None
    bill_year: int | None = None
    bill_date: str | None = None
    due_date: str | None = None
    payable_amount: float | None = None
    payable_after_due: float | None = None
    fixed_charges: float | None = None
    excel_bill_amount: float | None = None
    sanctioned_load_kw: float | None = None
    sanctioned_load_text: str | None = None
    connection_type: str | None = None
    tariff_category: str | None = None
    previous_reading: float | None = None
    current_reading: float | None = None
    units_consumed: float | None = None
    monthly_history: list[MonthlyUsage] = Field(default_factory=list)
    confidence: dict[str, float] = Field(default_factory=dict)
    raw_notes: list[str] = Field(default_factory=list)
    validation_issues: list[ValidationIssue] = Field(default_factory=list)


class GenerateWorkbookRequest(BaseModel):
    bills: list[BillExtraction]
    panel_wattage: float = 600.0


class ExtractionFailure(BaseModel):
    source_name: str
    message: str


class ExtractResponse(BaseModel):
    bills: list[BillExtraction]
    assumptions: list[str] = Field(default_factory=list)
    errors: list[ExtractionFailure] = Field(default_factory=list)


class WorkbookBuildResult(BaseModel):
    output_path: str
    output_name: str
    assumptions: list[str] = Field(default_factory=list)


class OpenAIExtractionEnvelope(BaseModel):
    bills: list[dict[str, Any]]
