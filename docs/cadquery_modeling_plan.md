# CadQuery Modeling Plan — V1

This repo uses **CadQuery as the source of truth** for the Universal Conical Filter Shaping Tool.

V1 workflow assumes **standard pre-seamed conical paper filters**, with common 02-class
papers and the 60° preset as the primary modeling reference.

---

## Modeling goals

V1 needs to support:
- indexed presets: **48° / 60° / 80°**
- parametric shell geometry
- tip locator and release mechanism
- cam ring and detent system
- export pipeline for STEP/STL/DXF/SVG

---

## Core modeling architecture

## 1. Parameters first
All geometry must derive from `cad/params.py`.

Never hardcode dimensions in component files.

Examples of parameter groups:
- shell geometry
- preset angles
- ring and cam geometry
- detent geometry
- seam-guide fin dimensions
- ejection system dimensions

---

## 2. Part modules

Each physical part gets its own builder in `cad/components/`.

Current component targets:
- `shell_half_l.py`
- `shell_half_r.py`
- `tip_insert_block.py`
- `cam_ring.py`
- `handle_housing.py`
- `overlap_fin.py`
- `ejection_rod.py`
- `base_cap.py`
- `handle_grip_insert.py`

### Expected interface

```python
def build(params=None, preset=None):
    ...
```

---

## 3. Assembly modules

Assemblies live in `cad/assemblies/`.

Targets:
- `mandrel_assy.py`
- `ring_assy.py`
- `ejection_assy.py`
- `full_assy.py`

### Expected interface

```python
def build(params=None, preset=None):
    ...
```

---

## 4. Utility modules

Utilities in `cad/utils/` should stay pure and reusable.

Current math/system helpers:
- `cone_math.py`
- `cam_geometry.py`
- `tolerances.py`

These are ideal for agent-driven development because they are:
- testable without CadQuery geometry
- deterministic
- easy to evolve before solids exist

---

## Preset strategy

Use **named presets**, not raw angle literals everywhere.

Current presets in `cad/params.py`:
- `PRESET_1` → 48°
- `PRESET_2` → 60°
- `PRESET_3` → 80°

### Modeling rule
- shell geometry depends on preset
- ring contains all preset logic
- handle / eject system are mostly preset-independent

---

## Build order

## Milestone 0 — math + validation
- cone conversions
- base radius checks
- cam dwell spacing
- detent proportions
- tolerance stack checks

## Milestone 1 — shell halves
Model:
- left shell
- right shell
- seam-relief / paper-registration features
- base tab and follower interface

## Milestone 2 — tip block + eject rod
Model:
- tip insert block
- tip dimple
- hinge bore
- ejection bore and rod

## Milestone 3 — cam ring
Model:
- outer ring body
- bore
- dwell positions
- transition geometry
- detent dimples
- labeling area / indicator logic

## Milestone 4 — handle housing
Model:
- ring capture
- detent pocket
- grip body
- angle window

## Milestone 5 — assemblies
Build:
- mandrel assembly
- ring assembly
- full assembly

## Milestone 6 — export automation
Generate:
- STEP
- STL
- DXF / SVG where relevant

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
```

---

## Testing priorities

Automated checks should cover:
- angle accuracy
- shell base diameter
- cam dwell radii
- detent geometry
- ejection stroke vs recess
- assembly clearances

---

## Agent implementation guidance

### Start here
1. `cad/params.py`
2. `cad/utils/cone_math.py`
3. `cad/utils/cam_geometry.py`
4. one simple component at a time

### Best first implemented parts
1. `cam_ring.py`
2. `tip_insert_block.py`
3. `overlap_fin.py`
4. `shell_half_l.py`
5. `shell_half_r.py`

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
