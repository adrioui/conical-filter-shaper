# Failure Mode & Effects Analysis (FMEA) — Rev 0.1

> Source: Design Spec §8 — `docs/design_spec.md`
> Extracted here for standalone reference.

For the full FMEA table, see `docs/design_spec.md` → §8 Failure Modes & Mitigations.

## Priority Failure Modes for V1 Validation Testing

(from spec §8.2 — run these tests at Phase 1 alpha)

| Priority | Test | Pass Criterion |
|----------|------|---------------|
| 1 | Angle accuracy at all 3 presets | ±0.5° across 5 tools |
| 2 | Filter tear rate at tip | Zero tears / 50 cycles / preset |
| 3 | Detent hold under forming load | No ring rotation at 5 N tangential |
| 4 | Filter insertion + ejection | Clean release ≤ 3 s: V60 / Timemore / Origami |
| 5 | Seam-guide repeatability | Seam position σ ≤ 0.5 mm across 20 cycles at the 10 mm setting |
| 6 | 500-cycle accelerated wear | Angle accuracy + detent feel unchanged at cycle 500 |
