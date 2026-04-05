# CLAUDE.md — conical-filter-shaper

> Agent entry-point. Read this first, then `HANDOFF.md`, then `cad/params.py` for current session context and dimensions.

---

## What This Repo Is

CadQuery (Python parametric CAD) source for the **Universal Conical Coffee Filter
Shaping Tool** — a three-preset angle-indexed mandrel targeting 48° / 60° / 80°
conical workflows with **standard pre-seamed cone papers**.

Full design spec: `docs/design_spec.md`  
Manufacturability & materials: `docs/manufacturability.md`  
Failure modes: `docs/fmea.md`  
Linux toolchain: `docs/toolchain_bluefin.md`

---

## Critical Conventions

### 1. Single Source of Truth
**ALL dimensions, tolerances, and material specs live in `cad/params.py`.**  
Never hardcode a number in a component file. Import from `params`.

### 1a. V1 Paper Workflow
**V1 assumes standard pre-seamed conical paper filters, not flat circular paper discs.**
Use common 02-class cone papers as the reference family. Keep 60° / P2 as the primary
workflow target; 48° and 80° remain compatibility presets pending physical validation.

### 2. Component Interface
Every file in `cad/components/` must expose:
```python
def build(params=None) -> cq.Workplane:
    """Docstring: origin convention, key dimensions, material."""
```
Every file in `cad/assemblies/` must expose:
```python
def build(params=None, preset=None) -> cq.Assembly:
    """Docstring: preset default, origin convention."""
```

### 3. Origin Conventions
| Part | Origin | Axis |
|------|--------|------|
| Shell halves | Apex (hinge point) at origin | Cone axis along +Z (apex up) |
| Tip insert block | Dimple center at origin | +Z toward button cap |
| Cam ring | Ring center at origin | +Z = up (toward shells) |
| Handle housing | Top face center at origin | +Z = up |
| Full assembly | Same as handle housing | +Z = up |

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
If you add a new component, add a corresponding test in `tests/test_components.py`.

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

# Validate geometry (tolerance stacks, clearances, interpenetration)
python scripts/validate_geometry.py

# Generate Bill of Materials (CSV + Excel)
python scripts/gen_bom.py

# Planned utilities (placeholders until real geometry exists)
python scripts/gen_drawings.py
python scripts/render_all.py

# Bump revision (updates params.REVISION, CHANGELOG.md, renames staged exports)
python scripts/bump_revision.py 0.2
```

---

## Key Geometry (from params.py)

| Parameter | Value |
|-----------|-------|
| Primary paper input | Standard pre-seamed conical papers (02-class reference) |
| Shell slant height | 82 mm (all presets) |
| Preset 1 / 48° base radius | 33.3 mm |
| Preset 2 / 60° base radius | 41.0 mm ← most common |
| Preset 3 / 80° base radius | 52.7 mm → max tool width 105.4 mm |
| Cam ring OD | 120 mm |
| Cam ring thickness | 14 mm |
| Handle OD | 42 mm |
| Handle length | 65 mm |
| Total tool height (80° preset) | ~166 mm |
| Angle accuracy target | ±0.5° included angle |

---

## File Naming — Exports

```
{part_name}_{revision}.{ext}
{assembly_name}_assy_{revision}.{ext}

Examples:
  shell_half_l_r0-1.step
  cam_ring_r0-1.step
  full_assy_r0-1.step
  overlap_fin_r0-1.dxf
  full_assy_iso_r0-1.png
  shell_half_l_section_r0-1.svg
```

Rules: all lowercase, underscores, revision token = `r{major}-{minor}`.

---

## Manufacturing Handoff

See `manufacturing/README.md` for how to package an RFQ.  
Critical dimensions: `manufacturing/inspection/critical_dims_v0-1.md`  
Indonesia sourcing: `docs/manufacturability.md` → §8.

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
- Edit `manufacturing/drawings/*.pdf` or `manufacturing/bom/*.xlsx` directly
- Change `params.REVISION` by hand — use `scripts/bump_revision.py`
