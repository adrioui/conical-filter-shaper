# Repository Structure

Annotated structure for `universal-filter-ruler`.

---

## Top level

```text
universal-filter-ruler/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── .python-version
├── .gitignore
├── cad/
├── tests/
├── scripts/
├── docs/
├── manufacturing/
├── refs/
├── exports/   # generated, gitignored
└── renders/   # generated, gitignored
```

---

## `cad/` — source of truth

```text
cad/
├── params.py           ✅ All design parameters, tolerances, materials
├── ruler_math.py      ✅ Geometric calculations for arm positions
├── components/
│   ├── __init__.py
│   ├── base_plate.py      ✅ T-slot base with magnetic track
│   ├── sliding_arm.py     ✅ Adjustable arm with vernier scale
│   ├── cam_lock.py        ✅ Eccentric cam lock mechanism
│   ├── magnetic_marker.py ✅ N52 magnet in colored housing
│   ├── ferrous_strip.py   ✅ Zinc-plated mild steel strip
│   └── ptfe_slide_strip.py ✅ Low-friction PTFE liner
├── assemblies/
│   ├── __init__.py
│   ├── arm_assy.py        ✅ Sliding arm + cam lock + PTFE
│   └── full_assy.py       ✅ Complete ruler assembly
└── utils/
    └── __init__.py
```

### Rules
- commit everything in `cad/`
- no magic numbers in component files
- all key dimensions come from `cad/params.py`

---

## `tests/`

Contains:
- `test_params.py` — parameter consistency and validity checks
- `test_ruler_math.py` — geometric calculation validation
- `test_components.py` — component building tests
- `test_assemblies.py` — assembly validation tests
- `test_tolerances.py` — tolerance band verification

Commit all of it.

---

## `scripts/`

Utility scripts for:
- `build_exports.py` — Generate STEP, STL, SVG, DXF exports
- `gen_bom.py` — Generate bill of materials CSV/XLSX
- `validate_geometry.py` — Geometry validation checks
- `bump_revision.py` — Revision management

Scripts may exist as stubs before full implementation.

---

## `docs/`

Human-facing design documentation:
- `design_spec.md` — Product specification (this replaces cone-specific spec)
- `manufacturability.md` — Materials, sourcing, COGS
- `repo_structure.md` — This file
- `fmea.md` — Failure modes analysis
- `adr/` — Architecture decision records

---

## `manufacturing/`

Vendor handoff material:
- `bom/bom_r1-0.csv` — Committed BOM
- Inspection docs
- Surface finish notes

Only source docs and CSV should be committed.
Generated PDFs/DXFs/XLSX stay gitignored.

---

## `refs/`

Reference material:
- Filter paper dimensions
- Competitor product notes
- Standards references

---

## `exports/` and `renders/`

Generated only.
Never edit manually.
Never treat as source-of-truth.

Typical contents:
- `exports/step/components/` — Component STEP files
- `exports/step/assemblies/` — Assembly STEP files
- `exports/stl/components/` — Component STL files
- `exports/svg/components/` — SVG section views
- `exports/dxf/components/` — DXF 2D profiles

---

## Naming conventions

### Python source
- `snake_case.py`

### Export files
- `{part_name}_r1-0.step`
- `{assembly_name}_r1-0.step`

### Parameters
- `UPPER_SNAKE_CASE_MM` — Lengths in mm
- `*_DEG` — Angles in degrees
- `*_N` — Forces in Newtons

---

## Commit policy

### Commit
- CAD source (`cad/`)
- tests (`tests/`)
- scripts (`scripts/`)
- markdown docs (`docs/`)
- CSV BOM (`manufacturing/bom/`)

### Do not commit
- Generated STEP/STL files
- Generated drawings
- Generated renders
- Local venv files
- Python cache (`__pycache__/`, `*.pyc`)

---

## Key Parameters (params.py)

```python
# BasePlate
BASE_LENGTH_MM = 200.0
BASE_WIDTH_MM = 120.0
BASE_THICKNESS_MM = 8.0

# Sliding Arms
ARM_LENGTH_MM = 150.0
ARM_WIDTH_MM = 25.0
ARM_THICKNESS_MM = 6.0

# Angle Range
ANGLE_MIN_DEG = 40.0
ANGLE_MAX_DEG = 85.0

# Magnetic Markers
MARKER_COUNT = 8  #4 colors × 2 each
```

---

*Last updated: 2026-04-06*