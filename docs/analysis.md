# Phase 1 to Phase 3 Analysis

## 1. Requirement summary

The task brief requires a working flow that:

1. Accepts a bill as PDF or image
2. Extracts bill values automatically with AI
3. Fills the provided Excel sheet
4. Preserves all formulas already present in the workbook
5. Returns a completed file ready for manual business use

## 2. Uploaded bill findings

The provided sample bills are Maharashtra `MSEDCL / Mahavitaran` residential bills. They are low-quality phone photos with bilingual Marathi and English text.

Fields visibly available across the samples:

- Utility name
- Consumer number
- Consumer name
- Address
- Mobile number
- Billing month
- Bill date
- Due date
- Payable amount
- Amount after due date
- Tariff / connection type
- Meter number
- Meter status
- Sanction load
- Previous reading
- Current reading
- Units consumed
- Reading dates
- Security deposit
- Historical monthly units chart

## 3. Excel workbook findings

The workbook contains exactly one sheet:

- `Pranay HOME`

Important structural facts:

- Sheet protection: `disabled`
- Formula cells exist and must be preserved in code
- The workbook is not blank; it contains two sample customer sections
- The bottom total rows aggregate both customer sections

## 4. Identified input cells

### Shared input

| Excel Cell | Excel Field |
|---|---|
| `C7` | Solar panel wattage used |

### Left customer section

| Bill Field | Excel Cell | Excel Field |
|---|---|---|
| Consumer Name | `D1` | Consumer Name |
| Consumer Number | `D2` | Consumer No |
| Fixed Charges | `D3` | Fixed Charges |
| Sanction Load | `D4` | Sanct. Load (kW) |
| Connection Type | `D5` | Connection Type |
| Month 1 label | `C9` | Month |
| Month 1 units | `D9` | Units |
| Month 2 label | `C10` | Month |
| Month 2 units | `D10` | Units |
| Month 3 label | `C11` | Month |
| Month 3 units | `D11` | Units |
| Month 4 label | `C12` | Month |
| Month 4 units | `D12` | Units |
| Month 5 label | `C13` | Month |
| Month 5 units | `D13` | Units |
| Month 6 label | `C14` | Month |
| Month 6 units | `D14` | Units |
| Month 7 label | `C15` | Month |
| Month 7 units | `D15` | Units |
| Month 8 label | `C16` | Month |
| Month 8 units | `D16` | Units |
| Month 9 label | `C17` | Month |
| Month 9 units | `D17` | Units |
| Month 10 label | `C18` | Month |
| Month 10 units | `D18` | Units |
| Month 11 label | `C19` | Month |
| Month 11 units | `D19` | Units |
| Month 12 label | `C20` | Month |
| Month 12 units | `D20` | Units |
| Current bill amount for unit-cost calculation | `E20` | Bill Amount |

### Right customer section

| Bill Field | Excel Cell | Excel Field |
|---|---|---|
| Consumer Name | `H1` | Consumer Name |
| Consumer Number | `H2` | Consumer No |
| Fixed Charges | `H3` | Fixed Charges |
| Sanction Load | `H4` | Sanct. Load (kW) |
| Connection Type | `H5` | Connection Type |
| Month 1 label | `G9` | Month |
| Month 1 units | `H9` | Units |
| Month 2 label | `G10` | Month |
| Month 2 units | `H10` | Units |
| Month 3 label | `G11` | Month |
| Month 3 units | `H11` | Units |
| Month 4 label | `G12` | Month |
| Month 4 units | `H12` | Units |
| Month 5 label | `G13` | Month |
| Month 5 units | `H13` | Units |
| Month 6 label | `G14` | Month |
| Month 6 units | `H14` | Units |
| Month 7 label | `G15` | Month |
| Month 7 units | `H15` | Units |
| Month 8 label | `G16` | Month |
| Month 8 units | `H16` | Units |
| Month 9 label | `G17` | Month |
| Month 9 units | `H17` | Units |
| Month 10 label | `G18` | Month |
| Month 10 units | `H18` | Units |
| Month 11 label | `G19` | Month |
| Month 11 units | `H19` | Units |
| Month 12 label | `G20` | Month |
| Month 12 units | `H20` | Units |
| Current bill amount for unit-cost calculation | `I20` | Bill Amount |

## 5. Formula cells

Left section formulas:

- `F20 = (E20-$D$3)/D20`
- `D22 = AVERAGE(D9:D21)`
- `E22 = AVERAGE(E14:E21)`
- `F22 = AVERAGE(F14:F21)` through shared formula
- `D23 = (D22*12*1.1)/1400`
- `D24 = D23/$C$7*1000`
- `D25 = ROUND(D24,0)*$C$7/1000`
- `D26 = D25/$C$7*1000`

Right section formulas:

- `J20 = (I20-$H$3)/H20`
- `H22 = AVERAGE(H9:H21)`
- `I22 = AVERAGE(I14:I21)`
- `J22 = AVERAGE(J14:J21)` through shared formula
- `H23 = (H22*12*1.1)/1400`
- `H24 = H23/$C$7*1000`
- `H25 = ROUND(H24,0)*$C$7/1000`
- `H26 = H25/$C$7*1000`

Grand totals:

- `D29 = SUM(25:25)`
- `D30 = SUM(26:26)` through shared formula

## 6. Dependencies

- `Unit Cost` depends on `Bill Amount`, `Fixed Charges`, and current-month `Units`
- `Average units` depends on the 12-month usage history
- `kW` depends on average units
- `Solar panels` depends on `kW` and panel wattage `C7`
- `Total solar capacity` and `Number of solar panels` depend on both customer sections

## 7. Important ambiguity

The template field labeled `Bill Amount` does not exactly match the prominent payable amount shown on the sample bill photos. Because of that, the application exposes this field to the user for review before export and falls back to the visible payable amount only when no better value is available.

## 8. Practical implementation decision

The app supports one or two uploaded bills:

- If one bill is uploaded, the app fills the left section and clears the right section.
- If two bills are uploaded, the app fills both sections.

This matches the actual workbook layout and keeps all original formulas intact.
