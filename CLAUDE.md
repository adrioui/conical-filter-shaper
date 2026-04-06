# CLAUDE.md — Universal Filter Ruler

> Agent entry-point. Read this first, then `cad/params.py` for current dimensions.

---

## What This Repo Is

CadQuery (Python parametric CAD) source for the **Universal Coffee Filter Ruler** —
a flat, adjustable angle ruler for folding circular coffee filter papers into precise
cone shapes. Two sliding aluminum arms on a flat base plate spread to any angle from
40° to 85°, locked by eccentric cam mechanisms.

Full design spec: `docs/design_spec.md`  
Manufacturability & materials: `docs/manufacturability.md`  
Linux toolchain: `docs/toolchain_bluefin.md`

---

## What This Is NOT

- ❌ Not a 3D cone mold, forming die, or hollow conical shell
- ❌ Not a mandrel or angle-indexed rotary tool
- ❌ The old "conical-filter-shaper" design has been superseded

Think: **sliding T-bevel gauge** purpose-built for coffee filter folding.

---

## Critical Conventions

### 1. Single Source of Truth
**ALL dimensions, tolerances, and material specs live in `cad/params.py`.**  
Never hardcode a number in a component file. Import from `params`.

### 2. Component Interface
Every file in `cad/components/` must expose:
```python
def build(params=None) -> cq.Workplane:
    """Docstring: origin convention, key dimensions, material."""
```
Every file in `cad/assemblies/` must expose:
```python
def build(params=None, **kwargs) -> cq.Assembly:
    """Docstring: origin convention, sub-assemblies."""
```
Stubs raise `NotImplementedError` until geometry is implemented.

### 3. Origin Conventions
| Part | Origin | Axis |
|------|--------|------|
| Base plate | Bottom face center at (0,0,0) | +Z up |
| Sliding arm | T-slot engagement midpoint at (0,0,0) | +X along arm length |
| Cam lock | Pivot bolt axis at (0,0,0) | +Z up (lever sweeps XY plane) |
| Magnetic marker | Bottom face center at (0,0,0) | +Z up |
| Full assembly | Base plate bottom face center at (0,0,0) | +Z up |

### 4. Exports Are Gitignored
`exports/` and `renders/` are never committed. Regenerate with:
```bash
python scripts/build_exports.py     # STEP + STL + SVG + DXF
python scripts/render_all.py        # PNG renders
```

### 5. Tests Must Pass Before Commit
```bash
pytest tests/ -v
```
Component stubs raise `NotImplementedError` → tests auto-skip via `build_or_skip()`.

---

## Quick Commands

```bash
# Install (Bluefin/Linux recommended path)
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Build all CAD exports (STEP / STL / SVG / DXF)
python scripts/build_exports.py

# Validate geometry
python scripts/validate_geometry.py

# Generate Bill of Materials (CSV + Excel)
python scripts/gen_bom.py

# Bump revision
python scripts/bump_revision.py 0.2
```

---

## Key Geometry (from Design Spec)

| Parameter | Value |
|-----------|-------|
| Base plate | 200mm × 120mm × 8mm, 6061-T6 Al |
| Sliding arm (×2) | 150mm × 25mm × 6mm, 6061-T6 Al |
| Angle range | 40° – 85° continuous |
| Angle resolution (scale) | 1° major, 0.5° vernier |
| T-slot fit | H7/h6 |
| Cam lock throw | 90° eccentric, ≥50 N clamp |
| Magnetic markers | 8× Ø6mm N52, 4 colors |
| Ferrous track strip | 180mm × 6mm × 1mm steel |
| Flatness tolerance | 0.05mm over 200mm |

---

## File Naming — Exports

```
{part_name}_{revision}.{ext}
{assembly_name}_assy_{revision}.{ext}

Examples:
  base_plate_r0-1.step
  sliding_arm_r0-1.step
  full_assy_r0-1.step
  base_plate_r0-1.dxf
```

Rules: all lowercase, underscores, revision token = `r{major}-{minor}`.

---

## Repo Structure

```
cad/
  params.py              ← Single source of truth for all dimensions
  components/
    base_plate.py        ← Flat base plate with T-slots + scale markings
    sliding_arm.py       ← Adjustable arm (×2)
    cam_lock.py          ← Eccentric cam lock mechanism (×2)
    magnetic_marker.py   ← Repositionable angle-preset marker (×8)
    ferrous_strip.py     ← Steel track strip for magnets
    ptfe_slide_strip.py  ← Optional PTFE liner for T-slot
  assemblies/
    arm_assy.py          ← One arm + cam lock
    full_assy.py         ← Base plate + both arm assemblies
  utils/
    ruler_math.py        ← Angle/arm geometry helpers (no CQ)
    tolerances.py        ← ISO 286 fit helpers (no CQ)
tests/
  conftest.py            ← Session fixtures (params, CQ marker)
  test_params.py         ← Ruler parameter consistency checks
  test_tolerances.py     ← ISO 286 fit tests
  test_components.py     ← Component build smoke tests
  test_assemblies.py     ← Assembly build smoke tests
```

---

## Separation of Concerns

| Layer | Changes when | Who touches it |
|-------|-------------|----------------|
| `params.py` | Design dims/tolerances change | Engineer / agent |
| `components/*.py` | Geometry implementation | Agent (run tests after) |
| `assemblies/*.py` | Assembly constraints | Agent (run tests after) |
| `tests/` | New parts, new failure modes | Agent + engineer |
| `scripts/` | Build tooling improvements | Agent |
| `docs/`, `refs/` | Design decisions, reference data | Engineer |
| `manufacturing/` | Vendor handoff prep | Engineer (via scripts) |
| `exports/`, `renders/` | **Generated only — never edit directly** | Scripts only |

---

## Do Not

- Commit anything under `exports/` or `renders/`
- Hardcode mm values in `components/` or `assemblies/` files
- Create a new part without a test in `tests/test_components.py`
- Change `params.REVISION` by hand — use `scripts/bump_revision.py`
- Import cone-math or cone-geometry helpers — that design is retired
