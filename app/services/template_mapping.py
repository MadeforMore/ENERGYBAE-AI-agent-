from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TemplateSlot:
    name: str
    consumer_name: str
    consumer_number: str
    fixed_charges: str
    sanctioned_load: str
    connection_type: str
    month_labels: list[str]
    units: list[str]
    bill_amount: str


LEFT_SLOT = TemplateSlot(
    name="left",
    consumer_name="D1",
    consumer_number="D2",
    fixed_charges="D3",
    sanctioned_load="D4",
    connection_type="D5",
    month_labels=[f"C{row}" for row in range(9, 21)],
    units=[f"D{row}" for row in range(9, 21)],
    bill_amount="E20",
)

RIGHT_SLOT = TemplateSlot(
    name="right",
    consumer_name="H1",
    consumer_number="H2",
    fixed_charges="H3",
    sanctioned_load="H4",
    connection_type="H5",
    month_labels=[f"G{row}" for row in range(9, 21)],
    units=[f"H{row}" for row in range(9, 21)],
    bill_amount="I20",
)

TEMPLATE_SLOTS = [LEFT_SLOT, RIGHT_SLOT]
PANEL_WATTAGE_CELL = "C7"
