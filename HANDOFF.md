# HANDOFF.md — Universal Filter Ruler

> Purpose: let a new session continue this project without losing context.
> Date: 2026-04-06
> Repo: `/var/home/adrifadilah/Learns/coffee/conical-filter-shaper`

---

## 1. Project Overview

### Product

A **precision aluminum adjustable angle ruler** for folding coffee filter papers into consistent cone shapes.

**Key Features:**
- Adjustable angle range: 40°–85° (included angle)
- Vernier scale for 0.5° resolution
- Magnetic markers for preset angle recall
- T-slot sliding mechanism with cam lock
- Laser-etched angle scales

### Tech Stack

- **CadQuery** — Python-native parametric CAD
- **pytest** — Test suite (194 tests passing)
- **Python 3.12** — Required for CadQuery compatibility
- **uv** — Package manager

---

## 2. Current State

### What's Implemented

✅ **Components (6):**
- `base_plate.py` — Aluminum plate with T-slots, magnetic track
- `sliding_arm.py` — Left/right arms with vernier scale
- `cam_lock.py` — Eccentric cam lock mechanism
- `magnetic_marker.py` — N52 magnet in colored housing
- `ferrous_strip.py` — Zinc-plated steel track insert
- `ptfe_slide_strip.py` — Low-friction PTFE liner

✅ **Assemblies (2):**
- `arm_assy.py` — Arm + cam lock + PTFE strip
- `full_assy.py` — Full ruler assembly

✅ **Tests (194):**
- Parameter validation
- Component dimensions
- Assembly clearances
- Math calculations (ruler_math.py)

✅ **Scripts:**
- `build_exports.py` — Export STEP/STL/SVG/DXF
- `gen_bom.py` — Generate bill of materials

✅ **Documentation:**
- `docs/design_spec.md` — Product specification (updated for ruler)
- `docs/manufacturability.md` — Materials, sourcing, COGS
- `docs/repo_structure.md` — Project structure
- `docs/fmea.md` — Failure modes analysis
- `docs/cadquery_modeling_plan.md` — Modeling approach

---

## 3. Quick Start

### Setup

```bash
cd /var/home/adrifadilah/Learns/coffee/conical-filter-shaper
source .venv/bin/activate
pytest tests/ -v
python scripts/build_exports.py
python scripts/gen_bom.py
```

### Run Tests

```bash
pytest tests/ --tb=short -q
# Expected: 194 passed
```

### Export CAD

```bash
python scripts/build_exports.py --formats step
# Outputs to exports/step/components/ and exports/step/assemblies/
```

---

## 4. Project Structure

```
conical-filter-shaper/
├── cad/
│   ├── params.py           # Design parameters
│   ├── ruler_math.py       # Geometric calculations
│   ├── components/        # 6 component files
│   ├── assemblies/        # 2 assembly files
│   └── utils/
├── tests/
│   ├── test_params.py
│   ├── test_components.py
│   ├── test_assemblies.py
│   ├── test_ruler_math.py
│   └── test_tolerances.py
├── scripts/
│   ├── build_exports.py
│   └── gen_bom.py
├── docs/
│   ├── design_spec.md
│   ├── manufacturability.md
│   ├── repo_structure.md
│   ├── fmea.md
│   ├── cadquery_modeling_plan.md
│   └── adr/
├── manufacturing/
│   └── bom/
│       ├── bom_r1-0.csv
│       └── bom_r1-0.xlsx
└── exports/
    └── step/
        ├── components/     # 6 ruler components
        └── assemblies/    # 2 ruler assemblies
```

---

## 5. Key Design Parameters

From `cad/params.py`:

| Parameter | Value |
|-----------|-------|
| `BASE_LENGTH_MM` | 200.0 |
| `BASE_WIDTH_MM` | 120.0 |
| `BASE_THICKNESS_MM` | 8.0 |
| `ARM_LENGTH_MM` | 150.0 |
| `ARM_WIDTH_MM` | 25.0 |
| `ARM_THICKNESS_MM` | 6.0 |
| `ANGLE_MIN_DEG` | 40.0 |
| `ANGLE_MAX_DEG` | 85.0 |
| `MARKER_COUNT` | 8 |
| `REVISION` | "1.0" |

---

## 6. Recent Changes (Stage6)

### Scripts Updated
- `build_exports.py`— Updated for ruler components/assemblies
- `gen_bom.py` — Updated for ruler BOM (10 rows)

### Documentation Updated
- `docs/design_spec.md` — Rewritten for Universal Filter Ruler
- `docs/manufacturability.md` — Updated for ruler manufacturing
- `docs/repo_structure.md` — Updated structure
- `docs/cadquery_modeling_plan.md` — Updated for ruler
- `docs/fmea.md` — Updated failure modes

### Project Config
- `pyproject.toml` — Changed name to "universal-filter-ruler"

### Bug Fixes
- Fixed `base_plate.py` edge fillet operation
- Fixed `full_assy.py` Assembly.toCompound() usage

### Removed
- Cone-specific ADRs (adr-002-pom-c-for-shells.md, adr-003-ball-detent-over-snap.md)

---

## 7. ApricotNotes

### Old Cone Files Present

The exports directory contains both old cone files and new ruler files. The old files remain from the previous "conical filter shaper" project. The new ruler files are:
- `base_plate_r1-0.step`
- `sliding_arm_r1-0.step`
- `cam_lock_r1-0.step`
- `magnetic_marker_r1-0.step`
- `ferrous_strip_r1-0.step`
- `ptfe_slide_strip_r1-0.step`
- `arm_assy_r1-0.step`
- `full_assy_r1-0.step`

### BOM Generated

```
Generating BOM — revision 1.0 (10 rows)
  ✅ CSV  → manufacturing/bom/bom_r1-0.csv
  ✅ XLSX → manufacturing/bom/bom_r1-0.xlsx
Done. Total unique parts: 10
```

### Test Results

```
194 passed, 7 warnings
```

---

## 8. Next Steps

1. **Prototype validation** — Print or CNC prototype for physical testing
2. **User testing** — Gather feedback on ergonomics and usability
3. **Drawing generation** — Add technical drawings for manufacturing
4. **Cost optimization** — Review BOM for cost reduction opportunities

---

## 9. Key Commands

```bash
# Activate environment
source .venv/bin/activate

# Run all tests
pytest tests/ -v

# Export STEP files
python scripts/build_exports.py --formats step

# Generate BOM
python scripts/gen_bom.py

# Validate geometry
python scripts/validate_geometry.py
```

---

*Last updated: 2026-04-06*  
*Revision: 1.0*