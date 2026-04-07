# Universal Coffee Filter Ruler

An adjustable stainless steel tool for folding coffee filter papers to precise cone angles and doubling as a compact dripper stand.

**First adjustable filter folding tool on the market.** Inspired by the Suprima SD1R ruler.

## What Is It?

A bevel-gauge style tool with two tapered SS304 stainless steel arms joined at a pivot:

```
  TOP VIEW (open at 60°):

          ╱‾‾‾‾‾‾‾‾‾‾╲
         ╱   filter     ╲
        ╱   paper on     ╲
       ╱     surface      ╲
      ╱    ╭── 02 ──╮     ╲
     ╱   ╭── 01 ──╮  ╲     ╲
    ╱  ╭── 03 ──╮  ╲  ╲     ╲
   ╱   ●─────────╲──╲──╲─────╲
       pivot      arm edges

  FOLDED:
  ┌──────────────┐
  │  130×80×4mm  │  ~125g
  │  pocket-sized │
  └──────────────┘
```

### Two Functions

1. **Filter Folding Guide**: Set angle → lay filter on arms → fold along straight inner edges → precise cone shape
2. **Dripper Stand**: Set angle → place dripper in V-cradle → arms support dripper rim

## Features

- 🔧 **Adjustable**: 40°–85° continuous range (covers SD1R through UFO)
- ☕ **Universal**: Works with V60-01, 02, 03 filter sizes
- 📐 **Protractor scale**: Laser-etched angle markings near pivot
- 🏷️ **Named presets**: SD1R (48°), SD1 (55°), V60 (60°), UFO (80°)
- ⭕ **Filter size arcs**: Etched marks at R=95mm (01), R=116mm (02), R=137mm (03)
- 🔩 **Simple**: Only 4 parts — 2 arms + bolt + washer + thumbscrew
- 🦾 **Durable**: SS304 stainless steel, food-grade, #4 brushed finish
- 📏 **Pocket-sized**: Folds to ~130×80×4mm, weighs ~125g

## Specifications

| Parameter | Value |
|-----------|-------|
| Arm length | 120mm (pivot to tip) |
| Arm width | 25mm (pivot) → 65mm (tip) |
| Arm thickness | 1.2mm |
| Material | SS304 stainless steel |
| Finish | #4 brushed |
| Angle range | 40°–85° |
| Pivot | M5 shoulder bolt + PTFE washer |
| Lock | M5 knurled thumbscrew |
| Weight | ~125g |
| Total parts | 4 unique (5 total incl. 2 arms) |
| Unit cost | ~$3.18 at 500 qty |

## Quick Start

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run tests
pytest -v

# Generate STEP/STL exports
python scripts/build_exports.py

# Exports appear in exports/step/, exports/stl/
```

## Project Structure

```
cad/
  params.py              # Design parameters
  components/
    ruler_arm.py         # Tapered SS304 arm with arc marks
    pivot_hinge.py       # M5 shoulder bolt assembly
    thumb_screw.py       # Knurled thumbscrew
  assemblies/
    ruler_assy.py        # Full ruler at configurable angle
  utils/
    ruler_math.py        # Cone angle math
tests/                   # pytest test suite
scripts/
  build_exports.py       # CAD export script
  gen_bom.py             # BOM generator
docs/
  design_spec.md         # Full design specification
exports/                 # Generated files (gitignored)
```

## Cone Angle Reference

| Dripper | Cone Angle | Sector Angle | Notes |
|---------|-----------|-------------|-------|
| SD1R (Suprima) | 48° | 146.5° | Steeper, more body |
| SD1 (Suprima) | ~55° | ~166° | Semi-immersion |
| V60 (Hario) | 60° | 180° | Standard |
| UFO Dripper | 80° | 231° | Shallow, clarity |

Formula: `sector_angle = 360° × sin(cone_half_angle)`

## Status

⚠️ **CAD reimplementation in progress.** The CadQuery geometry is being rewritten from narrow rectangular legs to properly tapered trapezoid arms. See `docs/design_spec.md` for the target specification.

## License

MIT

## Credits

Design inspired by the Suprima SD1R ruler by Hiro Lesmana.
