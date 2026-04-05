# Manufacturing Handoff — conical-filter-shaper

> This folder contains everything needed to issue an RFQ without sharing the CAD source.  
> All content here is **generated from `cad/params.py` and `scripts/`** — do not edit manually.

---

## How to Package an RFQ

### Step 1 — Regenerate outputs from source

```bash
# From repo root:
python scripts/build_exports.py         # → exports/step/components/*.step (once solids exist)
python scripts/gen_bom.py               # → manufacturing/bom/bom_r{rev}.csv + .xlsx
```

> Note: `scripts/gen_drawings.py` is scaffolded but not implemented yet. Drawing generation
> becomes meaningful only after the component solids stop being stubs.

### Step 2 — Assemble the vendor package

Zip the following into `rfq_v{rev}_{vendor}.zip`:

```
rfq_v0-1_vendor/
├── bom_r0-1.csv                      ← Bill of materials
├── surface_finish_notes.md           ← Ra callouts + anodize masking instructions
├── inspection/
│   ├── critical_dims_v0-1.md         ← Tolerance groups A–E (from spec §6)
│   └── fai_checklist_v0-1.md         ← First Article Inspection pass/fail
└── step/                              ← STEP files for each machined part
    ├── shell_half_l_r0-1.step
    ├── shell_half_r_r0-1.step
    ├── tip_insert_block_r0-1.step
    ├── cam_ring_r0-1.step
    ├── handle_housing_r0-1.step
    ├── ejection_rod_r0-1.step
    └── base_cap_r0-1.step
```

**Do not include:** CadQuery source, full assembly STEPs, or renders.

### Step 3 — Cover note to vendor

Include:
- Target material per part (see BOM)
- Surface finish per face (see `surface_finish_notes.md`)
- Anodize masking requirements (all tapped holes, detent dimples on cam ring rim)
- Critical tolerance group references (`inspection/critical_dims_v0-1.md` §A–§E)
- Requested: First Article Inspection Report (FAIR) before batch run

---

## Drawing Revision Convention

Drawing revision = `params.REVISION`. Never manually edit PDFs.  
Source for all dimensions: `cad/params.py`.  
To update revision: `python scripts/bump_revision.py {new_rev}` then re-run scripts above.

---

## Indonesia Sourcing Reference

See `docs/manufacturability.md` → §8 for vendor directory (Jakarta/Surabaya CNC shops,
anodize shops, SS 316L rod suppliers, POM-C sheet suppliers).
