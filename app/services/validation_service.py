from __future__ import annotations

from calendar import month_abbr
from datetime import date

from app.models.schema import BillExtraction, MonthlyUsage, ValidationIssue


def normalize_bill(extraction: BillExtraction) -> BillExtraction:
    extraction.consumer_number = clean_numeric_id(extraction.consumer_number)
    extraction.meter_number = clean_numeric_id(extraction.meter_number)
    extraction.monthly_history = normalize_monthly_history(extraction)

    if extraction.excel_bill_amount is None and extraction.payable_amount is not None:
        extraction.excel_bill_amount = extraction.payable_amount
        extraction.raw_notes.append(
            "Excel bill amount was missing, so payable amount was used as a fallback."
        )

    extraction.validation_issues = validate_bill(extraction)
    return extraction


def clean_numeric_id(value: str | None) -> str | None:
    if value is None:
        return None
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return digits or value.strip()


def normalize_monthly_history(extraction: BillExtraction) -> list[MonthlyUsage]:
    if extraction.bill_year is None:
        return extraction.monthly_history

    month_number = parse_month_number(extraction.bill_month_label)
    if month_number is None:
        return extraction.monthly_history

    expected = expected_month_window(extraction.bill_year, month_number)
    observed = {
        canonical_month_key(item.month_label): item
        for item in extraction.monthly_history
        if item.month_label
    }

    normalized: list[MonthlyUsage] = []
    for month_date in expected:
        key = month_date.strftime("%b %Y").lower()
        item = observed.get(key)
        if item is None:
            normalized.append(
                MonthlyUsage(
                    month_label=month_date.strftime("%b %Y"),
                    month_iso=month_date.strftime("%Y-%m"),
                    units=None,
                    confidence=0.0,
                )
            )
            continue

        normalized.append(
            MonthlyUsage(
                month_label=month_date.strftime("%b %Y"),
                month_iso=month_date.strftime("%Y-%m"),
                units=item.units,
                confidence=item.confidence,
            )
        )

    if extraction.units_consumed is not None and normalized:
        normalized[-1].units = extraction.units_consumed
        normalized[-1].confidence = max(normalized[-1].confidence, 0.85)

    return normalized


def expected_month_window(bill_year: int, bill_month: int) -> list[date]:
    months: list[date] = []
    year = bill_year
    month = bill_month
    for _ in range(12):
        months.append(date(year, month, 1))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    months.reverse()
    return months


def parse_month_number(value: str | None) -> int | None:
    if not value:
        return None
    cleaned = value.strip()[:3].title()
    months = {abbr: idx for idx, abbr in enumerate(month_abbr) if abbr}
    return months.get(cleaned)


def canonical_month_key(label: str) -> str:
    return " ".join(label.replace("-", " ").split()).strip().title().lower()


def validate_bill(extraction: BillExtraction) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if extraction.current_reading is not None and extraction.previous_reading is not None:
        expected_units = extraction.current_reading - extraction.previous_reading
        if extraction.units_consumed is not None and abs(expected_units - extraction.units_consumed) > 1:
            issues.append(
                ValidationIssue(
                    field="units_consumed",
                    severity="warning",
                    message=(
                        f"Units consumed ({extraction.units_consumed}) does not match "
                        f"current minus previous reading ({expected_units})."
                    ),
                )
            )

    if extraction.fixed_charges is None:
        issues.append(
            ValidationIssue(
                field="fixed_charges",
                message="Fixed charges were not extracted confidently. Please review before export.",
            )
        )

    if extraction.excel_bill_amount is None:
        issues.append(
            ValidationIssue(
                field="excel_bill_amount",
                message="Excel bill amount is missing. Review the bill breakup or enter it manually.",
            )
        )

    if len(extraction.monthly_history) != 12:
        issues.append(
            ValidationIssue(
                field="monthly_history",
                message="Monthly history is incomplete. The app will still export, but results may be less accurate.",
            )
        )

    return issues
