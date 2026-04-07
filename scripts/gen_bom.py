#!/usr/bin/env python3
"""
Generate Bill of Materials from cad/params.py component metadata.

Bevel Gauge with Tapered Arms — Revision r3-0
==============================================
4-item BOM:
  1. Tapered Arm (SS304, laser cut) ×2
  2. M5 Shoulder Bolt (SS316) ×1
  3. PTFE Washer 10×5.3×0.5mm ×1
  4. M5 Knurled Thumb Screw (SS304) ×1
  5. Cost target: ~$3.18/unit at 500 qty

Outputs:
    manufacturing/bom/bom_r3-0.csv   (committed — text-diffable)
    manufacturing/bom/bom_r3-0.xlsx  (gitignored — vendor-friendly)

Usage:
    python scripts/gen_bom.py
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path
from dataclasses import dataclass, asdict

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import cad.params as P

BOM_DIR = ROOT / "manufacturing" / "bom"
BOM_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class BomRow:
    item_no: int
    part_name: str
    qty: int
    material: str
    process: str
    source_file: str
    notes: str = ""


# Bevel Gauge with Tapered Arms Bill of Materials — Revision r3-0
BOM: list[BomRow] = [
    # ── Primary Structure ──────────────────────────────────────────────────────
    BomRow(
        1,
        "Tapered Arm",
        2,
        "SS304 Stainless Steel 1.2mm",
        "Laser cut → deburr → #4 brush finish → laser etch arc marks",
        "cad/components/ruler_arm.py",
        f"120×(25-65)×1.2mm tapered trapezoid, pivot hole Ø{P.ARM_PIVOT_HOLE_DIA_MM}mm, "
        f"arc marks 01/02/03, angle scale, edge radius R{P.ARM_EDGE_RADIUS_MM}mm; qty×2 = one ruler",
    ),
    # ── Pivot Hardware ──────────────────────────────────────────────────────────
    BomRow(
        2,
        "M5 Shoulder Bolt",
        1,
        "SS316 Stainless Steel",
        "Bought-in (machined)",
        "",
        f"Ø5mm thread, Ø{P.PIVOT_SHOULDER_DIAMETER_MM}mm shoulder, shoulder length {P.PIVOT_SHOULDER_LENGTH_MM}mm, "
        f"{P.PIVOT_BOLT_HEAD_DIA_MM}mm head; pivot spec: {P.PIVOT_BOLT_SPEC}",
    ),
    BomRow(
        3,
        "PTFE Washer",
        1,
        "PTFE 10×5.3×0.5mm",
        "Die cut",
        "",
        f"Ø{P.WASHER_OD_MM}mm OD, Ø{P.WASHER_ID_MM}mm ID (M5 clearance), {P.WASHER_THICKNESS_MM}mm thick; "
        "between arms for smooth rotation, self-lubricating",
    ),
    BomRow(
        4,
        "M5 Knurled Thumbscrew",
        1,
        "SS304 Stainless Steel",
        "Bought-in",
        "cad/components/thumb_screw.py",
        f"M5×0.8 thread, Ø{P.THUMB_SCREW_HEAD_DIAMETER_MM}mm knurled head, "
        f"{P.THUMB_SCREW_HEAD_HEIGHT_MM}mm head height; "
        "threads into pivot bolt to lock angle",
    ),
]

# ── Cost estimate ──────────────────────────────────────────────────────────────
UNIT_COST_ESTIMATE_USD: float = 3.18  # Target at 500 qty
UNIT_COST_CONDITION: str = "500 qty order"


def write_csv(path: Path) -> None:
    fields = ["item_no", "part_name", "qty", "material", "process", "source_file", "notes"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in BOM:
            writer.writerow(asdict(row))
    print(f"  ✅ CSV  → {path.relative_to(ROOT)}")


def write_xlsx(path: Path) -> None:
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"BOM r{P.REVISION}"
        headers = ["#", "Part Name", "Qty", "Material", "Process", "Source File", "Notes"]
        ws.append(headers)
        for row in BOM:
            ws.append([row.item_no, row.part_name, row.qty, row.material,
                       row.process, row.source_file, row.notes])
        # Cost summary row
        ws.append([])
        ws.append(["", "ESTIMATED UNIT COST", "", "", UNIT_COST_CONDITION, "", f"${UNIT_COST_ESTIMATE_USD:.2f}"])
        # Column widths
        ws.column_dimensions["A"].width = 4
        ws.column_dimensions["B"].width = 32
        ws.column_dimensions["C"].width = 5
        ws.column_dimensions["D"].width = 35
        ws.column_dimensions["E"].width = 45
        ws.column_dimensions["F"].width = 35
        ws.column_dimensions["G"].width = 60
        wb.save(path)
        print(f"  ✅ XLSX → {path.relative_to(ROOT)}")
    except ImportError:
        print("  ⚠️  openpyxl not installed — skipping XLSX. Run: pip install openpyxl")


if __name__ == "__main__":
    rev = P.REVISION.replace(".", "-")
    print(f"\n{'='*60}")
    print(f"  Bevel Gauge with Tapered Arms — BOM r{P.REVISION}")
    print(f"{'='*60}\n")
    print(f"  Generating BOM — revision {P.REVISION} ({len(BOM)} rows)\n")
    write_csv(BOM_DIR / f"bom_r{rev}.csv")
    write_xlsx(BOM_DIR / f"bom_r{rev}.xlsx")
    print(f"\n{'='*60}")
    print(f"  Total unique parts: {len(BOM)}")
    print(f"  Total parts per ruler: {sum(r.qty for r in BOM)}")
    print(f"  Estimated unit cost: ${UNIT_COST_ESTIMATE_USD:.2f} ({UNIT_COST_CONDITION})")
    print(f"{'='*60}\n")
    print("Done.")
