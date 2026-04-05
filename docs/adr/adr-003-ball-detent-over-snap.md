# ADR-003: Ball Detent Over Integral Snap Tab

**Date:** 2026-04-05  
**Status:** Accepted

## Context

The Angle-Set Ring must lock at 3 positions with a tactile click and sufficient hold
force to resist the ~5 N tangential forming load.

## Decision

Use a **ball detent** (SS 316L ball + SS 302 spring + M4 set screw retainer in handle
housing) engaging 3× dimples in the ring outer rim.

See spec §3.4 for full design. Key params: `DETENT_*` in `cad/params.py`.

## Reasons vs Alternatives

| Option | Click | Durability | Field adjust | V1 cost | Decision |
|--------|-------|-----------|-------------|---------|----------|
| Ball detent (selected) | ✅ Audible | 10,000+ cycles | ✅ Set screw | Low | **SELECTED** |
| POM integral snap tab | ✅ | ~500 cycles (wears) | ❌ | Zero | Rejected |
| Friction + set screw | ❌ No click | High | ✅ | Low | Rejected |

## Consequences

✅ Clear audible + tactile click  
✅ Field-adjustable preload (set screw depth)  
✅ 10,000-cycle target achievable (Hertzian contact stress well below SS 316L yield)  
❌ Spring wears over ~5–10 years daily use — user-replaceable with standard SS 302 spring  
❌ Detent dimples must be masked before anodize (see `manufacturing/surface_finish_notes.md`)

## Implementation Note

Dimple depth = 1.4 mm (~35% of 4.0 mm ball diameter). Too shallow = no click; too deep = won't release.
Tolerance: ±0.1 mm. This is `DETENT_DIMPLE_DEPTH_MM` in params.py.
