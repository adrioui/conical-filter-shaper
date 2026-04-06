# CadQuery Modeling Plan — V1

This repo uses **CadQuery as the source of truth** for the Universal Filter Ruler.

V1 workflow assumes **adjustable angle measurement for coffee filter folding** with angle range40°–85°.

---

## Modeling goals

V1 needs to support:
- adjustable angle range: **40°–85°**
- sliding arm mechanism with cam lock
- magnetic marker system for presets
- laser-etched angle and vernier scales
- export pipeline for STEP/STL/DXF/SVG

---

## Core modeling architecture

## 1. Parameters first
All geometry must derive from `cad/params.py`.

Never hardcode dimensions in component files.

Examples of parameter groups:
- base plate geometry
- sliding arm dimensions
- T-slot specifications
- cam lock geometry
- magnetic marker dimensions
- angle scale parameters

---

## 2. Part modules

Each physical part gets its own builder in `cad/components/`.

Current component targets:
- `base_plate.py` ✅
- `sliding_arm.py` ✅
- `cam_lock.py` ✅
- `magnetic_marker.py` ✅
- `ferrous_strip.py` ✅
- `ptfe_slide_strip.py` ✅

### Expected interface

```python
def build():
    """Build and return the component as a CadQuery Workplane."""
    ...
```

---

## 3. Assembly modules

Assemblies live in `cad/assemblies/`.

Targets:
- `arm_assy.py` ✅— Sliding arm + cam lock + PTFE
- `full_assy.py` ✅ — Complete ruler assembly

### Expected interface

```python
def build(angle_deg=60.0):
    """Build assembly at specified angle."""
    ...

def build(side="left"):
    """Build left or right arm assembly."""
    ...
```

---

## 4. Utility modules

Utilities in `cad/` should stay pure and reusable.

Current math helper:
- `ruler_math.py` — Geometric calculations for arm positions

This is ideal for agent-driven development because it is:
- testable without CadQuery geometry
- deterministic
- easy to evolve before solids exist

---

## Angle range strategy

Use **continuous angle range**, not discrete presets.

Range: 40°–85° (included angle between arm inner edges)

### Modeling rule
- arms pivot from center-top of base plate
- angle determines arm spread via `ruler_math.arm_position_at_angle()`
- magnetic markers allow users to mark preset angles for quick recall

---

## Build order

## Milestone 0 — math + validation ✅
- arm position calculations
- angle validation
- tolerance checks

## Milestone 1 — components ✅
- base_plate
- sliding_arm
- cam_lock
- magnetic_marker
- ferrous_strip
- ptfe_slide_strip

## Milestone 2 — assemblies ✅
- arm_assy
- full_assy

## Milestone 3 — documentation 🔄
- design_spec.md update
- manufacturability.md update
- BOM generation

## Milestone 4 — export automation
- STEP exports
- STL exports
- DXF/SVG for 2D profiles

---

## Build pipeline

The intended agent workflow is:

1. edit `cad/params.py`
2. run tests
3. run validation script
4. export CAD outputs

### Commands

```bash
pytest tests/ -v
python scripts/validate_geometry.py
python scripts/build_exports.py
python scripts/gen_bom.py
```

---

## Testing priorities

Automated checks should cover:
- angle range validation (40°–85°)
- arm position symmetry
- T-slot engagement fit
- cam lock position
- assembly clearances

---

## Agent implementation guidance

### Start here
1. `cad/params.py`
2. `cad/ruler_math.py`
3. One simple component at a time

### Implementation order
1. `base_plate.py` — Foundation with T-slots
2. `sliding_arm.py` — Moving part
3. `cam_lock.py` — Lock mechanism
4. `magnetic_marker.py` — Preset markers
5. `ferrous_strip.py` — Marker track
6. `ptfe_slide_strip.py` — Friction liner

Why:
- gives quick validation of exported solids
- surfaces geometry assumptions early
- enables simple bounding-box tests before harder assemblies

---

## Deliverable strategy

### Source-of-truth files
Commit:
- params
- component source
- assembly source
- tests
- scripts
- docs

### Generated artifacts
Do **not** commit:
- STEP
- STL
- render outputs
- generated drawings

These should always be reproducible from source.