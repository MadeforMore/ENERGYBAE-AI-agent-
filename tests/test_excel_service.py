from datetime import datetime
from pathlib import Path
import zipfile

from app.services.excel_service import build_workbooks, month_label_to_excel_date
from app.services.sample_data_service import get_sample_bill


def test_month_iso_to_excel_date():
    value = month_label_to_excel_date("Jan 2026", "2026-01")
    assert isinstance(value, datetime)
    assert value.year == 2026
    assert value.month == 1


def test_generated_workbook_contains_cached_formula_values():
    left = get_sample_bill(Path("assets/samples/bill_left.jpeg"), "bill_left.jpeg")
    assert left is not None
    output = build_workbooks([left], 600)
    with zipfile.ZipFile(output) as archive:
        xml = archive.read("xl/worksheets/sheet1.xml").decode("utf-8", errors="ignore")
    assert '<c r="D25" s="48"><f>ROUND(D24,0)*$C$7/1000</f><v>1.8</v></c>' in xml
    assert '<c r="D29" s="10"><f>sum(25:25)</f><v>1.8</v></c>' in xml
