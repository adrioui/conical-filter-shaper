# HANDOFF — Universal Coffee Filter Ruler

**Date**: 2026-04-07  
**Revision**: v3.0 (Bevel Gauge with Tapered Arms)  
**Status**: Design specified, CAD reimplementation needed

## Current State

The project has gone through 3 design iterations:

| Version | Design | Status |
|---------|--------|--------|
| v1.0 | Flat aluminum base plate with T-slot rails + sliding arms | ❌ Abandoned |
| v2.0 | Hinged V-shape with narrow rectangular SS304 legs (20mm × 155mm) | ❌ Abandoned |
| **v3.0** | **Bevel gauge with tapered SS304 arms (25→65mm × 120mm)** | **✅ Specified, needs CAD** |

### What's Done ✅

1. **Deep research** on SD1R ruler, competitive landscape, cone geometry math
   - SD1R ruler is a flat sector-shaped SS304 plate (filter guide + dripper stand)
   - NO adjustable filter folding tool exists on the market
   - Bevel gauge mechanism selected as optimal (simple, proven, pocket-sized)
   - Full research saved to Obsidian vault and `~/Learns/coffee/SD1R_RESEARCH_SYNTHESIS.md`

2. **Design specifications** written
   - Obsidian vault: `Everything Coffee/Projects/Universal Filter Ruler/`
     - Overview.md, Research Findings.md, Design Specifications.md, CAD Design Brief.md, Bill of Materials.md, Market Analysis.md
   - Repo: `docs/design_spec.md`

3. **Repo structure** exists (from v2.0)
   - CadQuery project with tests, export scripts, params
   - 132 tests passing (but testing OLD v2.0 geometry)

### What Needs Doing 🔧

1. **Rewrite `cad/params.py`** for v3.0:
   - Replace LEG_* params with ARM_* params
   - ARM_LENGTH=120, ARM_WIDTH_NARROW=25, ARM_WIDTH_WIDE=65, ARM_THICKNESS=1.2
   - Add ARC_01/02/03_RADIUS params (95, 116, 137mm)
   - Remove FOLD_MARK, PIVOT_MAGNET, etc.

2. **Rename + rewrite `cad/components/ruler_leg.py` → `ruler_arm.py`**:
   - Trapezoid shape (not rectangle)
   - Arc groove marks (not straight V-grooves at fixed distances)
   - Proper pivot hole positioning

3. **Simplify `cad/components/pivot_hinge.py`**:
   - Remove magnet, simplify to just shoulder bolt
   - Or rename to pivot_bolt.py

4. **Update `cad/assemblies/ruler_assy.py`**:
   - Use new tapered arms
   - Proper Z-stacking (arm + washer + arm + screw)
   - Angle-based rotation

5. **Update `cad/utils/ruler_math.py`**:
   - Add cone angle ↔ sector angle conversion
   - Add V-opening width calculator
   - Keep angle range validation

6. **Update all tests** for new geometry

7. **Regenerate STEP exports** (current r2-0 files are WRONG geometry)

8. **Update `scripts/build_exports.py`** for renamed components

### What's in the Repo (File Inventory)

```
conical-filter-shaper/
  CLAUDE.md              ← Updated for v3.0
  README.md              ← Updated for v3.0
  HANDOFF.md             ← This file
  pyproject.toml         ← Build config (OK)
  cad/
    params.py            ← ⚠️ NEEDS REWRITE for v3.0 params
    components/
      ruler_leg.py       ← ⚠️ RENAME to ruler_arm.py + rewrite
      pivot_hinge.py     ← ⚠️ SIMPLIFY (remove magnet)
      thumb_screw.py     ← OK (keep knurled thumbscrew)
    assemblies/
      ruler_assy.py      ← ⚠️ UPDATE for tapered arms
    utils/
      ruler_math.py      ← ⚠️ ADD cone angle functions
  tests/
    test_components.py   ← ⚠️ UPDATE for new arm geometry
    test_assemblies.py   ← ⚠️ UPDATE for new assembly
    test_params.py       ← ⚠️ UPDATE for new params
    test_ruler_math.py   ← ⚠️ UPDATE for new math functions
  scripts/
    build_exports.py     ← ⚠️ UPDATE component names
    gen_bom.py           ← ⚠️ UPDATE for 4-part BOM
  docs/
    design_spec.md       ← Updated for v3.0
  exports/               ← ⚠️ STALE (r2-0 = wrong geometry, delete + regenerate)
```

### Key Design Parameters (v3.0)

| Parameter | Value | Notes |
|-----------|-------|-------|
| ARM_LENGTH_MM | 120.0 | Pivot hole to tip |
| ARM_WIDTH_NARROW_MM | 25.0 | At pivot end |
| ARM_WIDTH_WIDE_MM | 65.0 | At tip end |
| ARM_THICKNESS_MM | 1.2 | SS304 sheet |
| ARC_01_RADIUS_MM | 95.0 | V60-01 filter size |
| ARC_02_RADIUS_MM | 116.0 | V60-02 filter size |
| ARC_03_RADIUS_MM | 137.0 | V60-03 filter size |
| ANGLE_MIN_DEG | 40.0 | Minimum operating angle |
| ANGLE_MAX_DEG | 85.0 | Maximum operating angle |
| BOLT_SHOULDER_DIA_MM | 8.0 | M5 shoulder bolt |
| WASHER_THICKNESS_MM | 0.5 | PTFE washer |
| THUMB_HEAD_DIA_MM | 15.0 | Knurled thumbscrew head |

### Obsidian Vault Location

`~/Tooling/cognitive-vault/Everything Coffee/Projects/Universal Filter Ruler/`

Contains 6 notes: Overview, Research Findings, Design Specifications, CAD Design Brief, Bill of Materials, Market Analysis

### Next Action

Implement the v3.0 CAD geometry in CadQuery. Start with `params.py`, then `ruler_arm.py`, then assembly. Run tests after each step.
