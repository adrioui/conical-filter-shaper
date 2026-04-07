# CLAUDE.md — Universal Coffee Filter Ruler

## What This Project Is

Parametric CadQuery model of an **adjustable coffee filter folding ruler + dripper stand**.

Inspired by the Suprima SD1R ruler concept. Bevel-gauge style: two tapered SS304 stainless steel arms joined at a pivot with knurled thumbscrew. First adjustable filter folding tool on the market.

## Design Form

**Bevel gauge (T-bevel)** with two tapered flat arms:
- Arms: 120mm long, tapered from 25mm (pivot) to 65mm (tip), 1.2mm thick
- Material: SS304 stainless steel, #4 brushed finish
- Pivot: M5 shoulder bolt + PTFE washer + knurled thumbscrew
- Angle range: 40°–85° continuous
- Folded: ~130 × 80 × 4mm, ~125g
- Total parts: 4 unique (2 identical arms + bolt + washer + thumbscrew)

## How It Works

1. **Filter folding guide**: Open arms to target angle → lay filter on arms → fold along straight inner edges
2. **Dripper stand**: Open to dripper angle → place dripper in V-cradle → arms support rim

## Repository Structure

```
cad/
  params.py              # All design parameters
  components/
    ruler_arm.py         # Tapered arm (trapezoid, pivot hole, arc marks)
    pivot_hinge.py       # M5 shoulder bolt assembly
    thumb_screw.py       # M5 knurled thumbscrew
  assemblies/
    ruler_assy.py        # Two arms + pivot + screw at adjustable angle
  utils/
    ruler_math.py        # Cone angle ↔ sector geometry calculations
tests/
  test_components.py     # Component build tests
  test_assemblies.py     # Assembly tests at various angles
  test_params.py         # Parameter validation
  test_ruler_math.py     # Math function tests
scripts/
  build_exports.py       # STEP/STL/SVG export
  gen_bom.py             # BOM CSV generation
exports/                 # Generated CAD files (gitignored)
docs/
  design_spec.md         # Full design specification
```

## Key Parameters (cad/params.py)

```python
ARM_LENGTH_MM = 120.0        # Pivot to tip
ARM_WIDTH_NARROW_MM = 25.0   # At pivot end
ARM_WIDTH_WIDE_MM = 65.0     # At tip end
ARM_THICKNESS_MM = 1.2       # SS304 sheet
ARM_EDGE_RADIUS_MM = 0.3     # Deburred edges
ARC_01_RADIUS_MM = 95.0      # V60-01 filter size mark
ARC_02_RADIUS_MM = 116.0     # V60-02 filter size mark
ARC_03_RADIUS_MM = 137.0     # V60-03 filter size mark
ANGLE_MIN_DEG = 40.0
ANGLE_MAX_DEG = 85.0
```

## Build & Test

```bash
source .venv/bin/activate
pytest -v                           # Run all tests
python scripts/build_exports.py     # Generate STEP/STL exports
```

## Design Status

⚠️ **CAD NEEDS REIMPLEMENTATION**: The current CadQuery code still has the OLD design (narrow rectangular legs). It needs to be rewritten for tapered trapezoid arms with arc marks, protractor scale, and proper pivot positioning. See `docs/design_spec.md` and the Obsidian vault `CAD Design Brief` for specifications.

## Named Angle Presets

| Dripper | Cone Angle | Use Case |
|---------|-----------|----------|
| SD1R | 48° | Steeper, more body |
| SD1 | 55° | Semi-immersion |
| V60 | 60° | Standard pour-over |
| UFO | 80° | Shallow, clarity-focused |
