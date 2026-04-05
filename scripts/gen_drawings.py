#!/usr/bin/env python3
"""
Planned drawing generation entrypoint.

Current status:
- scaffold only
- nominal component geometry now exists
- but no authoritative drawing generation pipeline is implemented yet

Future scope:
- generate DXF/SVG/PDF drawings from implemented CadQuery geometry
- write outputs into manufacturing/drawings/
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAWINGS_DIR = ROOT / "manufacturing" / "drawings"
DRAWINGS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    print("gen_drawings.py is scaffolded but not implemented yet.")
    print("Reason: nominal solids exist, but no trustworthy drawing extraction/dimensioning pipeline is wired up yet.")
    print(f"Target output directory: {DRAWINGS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
