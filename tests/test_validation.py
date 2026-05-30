from app.models.schema import BillExtraction, MonthlyUsage
from app.services.validation_service import normalize_bill


def test_normalize_monthly_history_builds_twelve_months():
    bill = BillExtraction(
        source_name="sample.jpg",
        bill_month_label="Jan",
        bill_year=2026,
        units_consumed=25,
        monthly_history=[
            MonthlyUsage(month_label="Feb 2025", units=99, confidence=0.8),
            MonthlyUsage(month_label="Jan 2026", units=23, confidence=0.7),
        ],
    )

    normalized = normalize_bill(bill)

    assert len(normalized.monthly_history) == 12
    assert normalized.monthly_history[0].month_label == "Feb 2025"
    assert normalized.monthly_history[-1].month_label == "Jan 2026"
    assert normalized.monthly_history[-1].units == 25


def test_payable_amount_falls_back_to_excel_bill_amount():
    bill = BillExtraction(
        source_name="sample.jpg",
        payable_amount=1460.0,
    )

    normalized = normalize_bill(bill)

    assert normalized.excel_bill_amount == 1460.0
