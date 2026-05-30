from pathlib import Path

from app.services.sample_data_service import get_sample_bill


def test_left_sample_is_detected():
    bill = get_sample_bill(
        path=Path("assets/samples/bill_left.jpeg"),
        source_name="bill_left.jpeg",
    )
    assert bill is not None
    assert bill.consumer_number == "439320095567"
    assert bill.units_consumed == 25
