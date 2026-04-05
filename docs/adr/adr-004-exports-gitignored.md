# ADR-004: Generated Exports Are Gitignored

**Date:** 2026-04-05  
**Status:** Accepted

## Decision

STEP, STL, SVG, DXF, PDF, and PNG render files are **not committed to git**.  
They are regenerated on demand via `scripts/build_exports.py`.

## Reasons

- Binary files bloat repo history — a single STEP file can be 2–10 MB
- Every geometry change would generate a new binary blob with no useful diff
- Agents and CI can regenerate them on demand in seconds
- Manufacturing handoff uses a zip snapshot, not a git checkout

## How to Get Exports

```bash
python scripts/build_exports.py   # STEP + STL + SVG + DXF (once solids exist)
python scripts/render_all.py      # PNG renders (placeholder entrypoint today)
```

## What IS Committed

- `manufacturing/bom/bom_r{rev}.csv` — text-diffable, useful in PR reviews
- `manufacturing/inspection/*.md` — human-readable tolerance specs
- `manufacturing/surface_finish_notes.md`

## For Long-Term Artifact Retention

Use **Git LFS** for renders if a persistent artifact trail is needed:
```bash
git lfs track "renders/**/*.png"
```

Or use CI (GitHub Actions) to publish export artifacts on each tagged commit.
