# Critical Dimensions — Rev 0.1

> Extracted from `cad/params.py` tolerance groups.  
> Use for First Article Inspection (FAI). Verify these dimensions before accepting batch.

---

## Group A — Angle-Critical (define cone geometry)

| Dimension | Nominal | Tolerance | Part | Consequence of error |
|-----------|---------|-----------|------|---------------------|
| Cam track dwell radius — P1 | 33.3 mm | ± 0.10 mm | Cam Ring | ±0.17° in included angle |
| Cam track dwell radius — P2 | 41.0 mm | ± 0.10 mm | Cam Ring | ±0.14° |
| Cam track dwell radius — P3 | 52.7 mm | ± 0.10 mm | Cam Ring | ±0.11° |
| Shell base follower pin OD | 4.0 mm | h6 (−0.000/−0.008) | Shell L, R | Pin play in track → slack in angle |
| Shell slant length (apex to base pin) | 82.0 mm | ± 0.20 mm | Shell L, R | ±0.14° per mm error |

**Target:** ±0.5° included angle at each preset. Verify with angle gauge after assembly.

---

## Group B — Tip Locator (filter centering)

| Dimension | Nominal | Tolerance |
|-----------|---------|-----------|
| Tip dimple position from cone axis | 0 mm (on axis) | ±0.30 mm concentricity |
| Tip dimple depth | 2.0 mm | +0.15 / −0.00 mm |
| Tip dimple included angle | 60° | ±5° (non-critical) |
| Ejection rod tip recess at rest | −1.5 mm (recessed below tip face) | ±0.30 mm |

---

## Group C — Seam Guide Fin (paper seam control)

| Dimension | Nominal | Tolerance |
|-----------|---------|-----------|
| Fin slot width (Shell R) | 0.55 mm | +0.05 / −0.00 mm |
| Fin blade thickness | 0.50 mm | ±0.02 mm |
| Fin position marks (5/7.5/10/12.5/15 mm) | Per mark | ±0.30 mm |
| Fin pull-out force at each serration | 10 N | ±4 N (soft limit; verify with spring scale) |

---

## Group D — Rotary Interfaces (ring in housing)

| Dimension | Nominal | Tolerance | Fit |
|-----------|---------|-----------|-----|
| Cam Ring OD | 120.0 mm | −0.00 / −0.05 mm | Clearance in housing bore |
| Housing ring bore | 120.2 mm | +0.00 / +0.05 mm | ~0.10–0.25 mm diametral clearance |
| Ring axial float (with PTFE washers) | 0.5 mm per washer | ±0.10 mm | Controls ring wobble |
| Detent dimple depth (ring rim) | 1.4 mm | ±0.10 mm | **Critical — see surface_finish_notes.md** |
| Detent dimple radius | 2.2 mm | ±0.10 mm | |

---

## Group E — Ejection System

| Dimension | Nominal | Tolerance | Fit |
|-----------|---------|-----------|-----|
| Ejection rod OD | 3.0 mm | h6 (−0.006 / −0.014 mm) | Sliding in H7 bore |
| Tip insert axial bore | 3.0 mm | H7 (+0.010 / +0.025 mm) | |
| Ejection stroke | 5.0 mm | ±0.5 mm | Non-critical |

---

## V1 Validation Tests (from spec §8.2)

Before accepting batch, perform:

| Priority | Test | Pass Criterion |
|----------|------|---------------|
| 1 | Angle accuracy at all 3 presets | Measured included angle ±0.5° across 5 tools |
| 2 | Filter tear rate at tip | Zero tears in 50 shaping cycles per preset |
| 3 | Detent hold under forming load | No ring rotation with 5 N tangential load at rim |
| 4 | Filter insertion + ejection | Clean release in ≤ 3 s across V60 / Timemore / Origami |
| 5 | Seam-guide repeatability | Seam position σ ≤ 0.5 mm across 20 cycles at the 10 mm setting |
