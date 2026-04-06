#!/usr/bin/env python3
"""
Generate Bill of Materials from cad/params.py component metadata.

Outputs:
    manufacturing/bom/bom_r{rev}.csv   (committed — text-diffable)
    manufacturing/bom/bom_r{rev}.xlsx  (gitignored — vendor-friendly)

Usage:
    python scripts/gen_bom.py
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict

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


# Universal Filter Ruler Bill of Materials
# Reference: vault/Bill of Materials.md
BOM: list[BomRow] = [
    # ── Machined Components ──────────────────────────────────────────────────────
    BomRow(1, "Base Plate", 1, P.BASE_MATERIAL, P.BASE_PROCESS,
           "cad/components/base_plate.py",
           f"{P.BASE_LENGTH_MM}×{P.BASE_WIDTH_MM}×{P.BASE_THICKNESS_MM}mm"),
    BomRow(2, "Sliding Arm", 2, P.ARM_MATERIAL, P.ARM_PROCESS,
           "cad/components/sliding_arm.py",
           f"{P.ARM_LENGTH_MM}×{P.ARM_WIDTH_MM}×{P.ARM_THICKNESS_MM}mm"),
    BomRow(3, "Cam Lock Assembly", P.CAM_COUNT, P.CAM_MATERIAL, P.CAM_LEVER_MATERIAL,
           "cad/components/cam_lock.py",
           f"{P.CAM_THROW_DEG}° throw, {P.CAM_LEVER_LENGTH_MM}mm lever"),
    # ── Magnetic System ──────────────────────────────────────────────────────────
    BomRow(4, "Magnetic Marker", P.MARKER_COUNT, P.MARKER_MATERIAL, P.MARKER_PROCESS,
           "cad/components/magnetic_marker.py",
           f"Ø{P.MARKER_DIAMETER_MM}×{P.MARKER_HEIGHT_MM}mm, {P.MARKER_COUNT} total (4 colors×2)"),
    BomRow(5, "Ferrous Track Strip", 1, P.MARKER_TRACK_INSERT_SPEC, "Laser cut",
           "cad/components/ferrous_strip.py",
           f"{P.MARKER_TRACK_LENGTH_MM}×{P.MARKER_TRACK_WIDTH_MM}×{P.MARKER_TRACK_RECESS_DEPTH_MM}mm"),
    # ── Sliding System ───────────────────────────────────────────────────────────
    BomRow(6, "PTFE Slide Strip", P.PTFE_COUNT, P.PTFE_MATERIAL, "Die cut",
           "cad/components/ptfe_slide_strip.py",
           f"{P.PTFE_LENGTH_MM}×{P.PTFE_WIDTH_MM}×{P.PTFE_THICKNESS_MM}mm"),
    # ── Hardware ────────────────────────────────────────────────────────────────
    BomRow(7, "M3×8 SHCS", P.FASTENER_M3_SHCS_QTY, "SS A2-70", "Bought-in",
           "", P.FASTENER_M3_SHCS_SPEC),
    BomRow(8, "M5 Shoulder Bolt", P.FASTENER_M5_SHOULDER_QTY, "SS 316", "Bought-in",
           "", P.FASTENER_M5_SHOULDER_SPEC),
    BomRow(9, "Belleville Washer M5", P.FASTENER_BELLEVILLE_QTY, "Spring steel", "Bought-in",
           "", P.FASTENER_BELLEVILLE_SPEC),
    BomRow(10, "Silicone Foot Pad", P.FOOT_PAD_COUNT, P.FOOT_PAD_MATERIAL, "Bought-in",
           "", f"Ø{P.FOOT_PAD_DIAMETER_MM}mm, adhesive-backed"),
]


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
        # Column widths
        ws.column_dimensions["B"].width = 28
        ws.column_dimensions["D"].width = 35
        ws.column_dimensions["G"].width = 40
        wb.save(path)
        print(f"  ✅ XLSX → {path.relative_to(ROOT)}")
    except ImportError:
        print("  ⚠️  openpyxl not installed — skipping XLSX. Run: pip install openpyxl")


if __name__ == "__main__":
    rev = P.REVISION.replace(".", "-")
    print(f"\nGenerating BOM — revision {P.REVISION} ({len(BOM)} rows)\n")
    write_csv(BOM_DIR / f"bom_r{rev}.csv")
    write_xlsx(BOM_DIR / f"bom_r{rev}.xlsx")
    print(f"\nDone. Total unique parts: {len(BOM)}")