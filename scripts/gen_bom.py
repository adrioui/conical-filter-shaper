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


BOM: list[BomRow] = [
    BomRow(1,  "Half-Shell L",             1, P.SHELL_MATERIAL,          P.SHELL_PROCESS,         "cad/components/shell_half_l.py"),
    BomRow(2,  "Half-Shell R",             1, P.SHELL_MATERIAL,          P.SHELL_PROCESS,         "cad/components/shell_half_r.py", "Includes fin slot"),
    BomRow(3,  "Tip Insert Block",         1, P.TIP_MATERIAL,            P.TIP_PROCESS,           "cad/components/tip_insert_block.py"),
    BomRow(4,  "Apex Hinge Pin",           1, "SS 316L",                 "Shoulder bolt",          "", P.HINGE_PIN_SPEC),
    BomRow(5,  "Cam Follower Pin L",       1, "SS 316L",                 "Shoulder bolt",          "", P.FOLLOWER_PIN_SPEC),
    BomRow(6,  "Cam Follower Pin R",       1, "SS 316L",                 "Shoulder bolt",          "", P.FOLLOWER_PIN_SPEC),
    BomRow(7,  "Angle-Set Ring",           1, P.CAM_RING_MATERIAL,       P.CAM_RING_PROCESS,      "cad/components/cam_ring.py", "Mask detent dimples before anodize"),
    BomRow(8,  "Handle Housing",           1, P.HOUSING_MATERIAL,        P.HOUSING_PROCESS,       "cad/components/handle_housing.py", "Mask all tapped holes before anodize"),
    BomRow(9,  "Handle Grip Insert",       1, "NBR-70 or TPU Shore-A70", "Moulded / laser-cut",   "cad/components/handle_grip_insert.py"),
    BomRow(10, "Detent Ball",              1, "SS 316L grade G25",        "Bought-in",             "", f"Ø{P.DETENT_BALL_DIAMETER_MM} mm"),
    BomRow(11, "Detent Spring",            1, "SS 302",                  "Bought-in",             "", f"FL {P.DETENT_SPRING_FREE_LENGTH_MM} mm"),
    BomRow(12, "Detent Set Screw",         1, "SS 316L",                 "Bought-in",             "", P.DETENT_SETSCREW_SPEC),
    BomRow(13, "Seam Guide Fin",          1, P.FIN_MATERIAL,            P.FIN_PROCESS,           "cad/components/overlap_fin.py"),
    BomRow(14, "Ejection Push Rod",        1, P.EJECTION_ROD_MATERIAL,   P.EJECTION_ROD_PROCESS,  "cad/components/ejection_rod.py"),
    BomRow(15, "Ejection Return Spring",   1, "SS 302",                  "Bought-in",             "", f"FL {P.EJECTION_SPRING_FREE_LENGTH_MM} mm"),
    BomRow(16, "Ejection Button Cap",      1, P.EJECTION_BUTTON_MATERIAL, "CNC turned",           "cad/components/ejection_rod.py (button sub-feature)"),
    BomRow(17, "Base Cap / Ring Retainer", 1, "6061-T6 Al, Type II anodize", "CNC turned + anodize", "cad/components/base_cap.py"),
    BomRow(18, "Ring Bearing Washer",      2, "PTFE",                    "Punched",               "", P.PTFE_WASHER_SPEC),
    BomRow(19, "Assembly Screws M3 SHCS",  4, "SS 316L",                 "Bought-in",             "", P.ASSEMBLY_SCREWS_SPEC),
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
        ws.column_dimensions["D"].width = 40
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
