# HANDOFF.md — Universal Conical Filter Shaping Tool

> Purpose: let a new session continue this project without losing context.
> Date: 2026-04-05
> Repo: `/var/home/adrifadilah/Learns/coffee/conical-filter-shaper`

---

## 1. Current objective

Build a **sellable, universal conical coffee filter shaping tool** for specialty coffee users.

The product direction is:
- **premium coffee nerd tool**, not a cheap generic ruler
- **CadQuery** as CAD source of truth
- **FreeCAD** as viewer/checker/optional drawing tool
- **Linux + AI-agent friendly** workflow

Core product idea:
- indexed presets: **48° / 60° / 80°**
- input paper = **standard pre-seamed conical filters**
- shape paper consistently
- support seam repeatability / relief
- transfer into brewer cleanly
- release tool without pulling paper back out

---

## 2. Important context from the user

The user wants:
- **free + open-source CAD**
- must run on **Linux**
- must be **easy for an AI agent to use**
- likely productizable / sellable, not just a one-off DIY hack

This is why the stack chosen is:
- **CadQuery first**
- **FreeCAD second**

---

## 3. What was done in this session

### Product/design work
We explored and converged on:
- a **universal conical filter shaping system**
- best V1 mechanism direction: **indexed split-shell mandrel**
- presets: **48 / 60 / 80 degrees**
- key mechanism ideas:
  - split forming shells
  - indexed angle-set ring
  - ball detent
  - tip locator
  - seam-relief guide
  - adjustable seam-guide fin
  - eject / release pin
  - wetting / vent channels

### Research performed
We compared against:
- **SD1R ruler**
- **UFO folding template**
- **OREA Negotiator / Tulip**
- **Filter Paper Applicator – Conical**

Conclusion:
- there is a real niche for a **conical equivalent of OREA-style shaping tooling**
- user wants something that could plausibly be sold

### CAD workflow work
We decided:
- **CadQuery = source of truth**
- **FreeCAD = visual inspection / interoperability**
- on Bluefin/Fedora-like immutable Linux, use:
  - `uv` + **Python 3.12** for CadQuery
  - **FreeCAD Flatpak or extracted AppImage**

### Repo scaffold work
A CAD repo scaffold exists and was cleaned up:
- packaging backend fixed
- Python version pinned for compatibility
- missing docs/scripts added as placeholders
- internal doc links fixed
- test scaffold made honest about stub geometry
- cam-track 180° per-follower logic corrected
- detent wording made consistent

### Validation performed
A local venv was created and validated.

Commands run successfully:
```bash
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e '.[dev]'
pytest tests -q
python scripts/validate_geometry.py
python scripts/gen_bom.py
python scripts/gen_drawings.py
python scripts/render_all.py
```

Current validated result after implementation follow-up:
- **74 passed**
- **0 xfailed**
- **0 skipped**
- `python scripts/validate_geometry.py` passes
- `python scripts/build_exports.py` exports both components and assemblies successfully

---

## 4. Current repository status

### Repo path
`/var/home/adrifadilah/Learns/coffee/conical-filter-shaper`

### Current state
This repo is now a **working pre-prototype CadQuery model + validated math/params/tests layer**.

What is real now:
- project structure
- params system
- math helpers
- tolerance checks
- geometry validation script
- BOM generation
- export pipeline for components and assemblies
- nominal CadQuery solids for all current components
- nominal CadQuery assemblies for the tool stack
- clean Linux toolchain docs

What is **not** implemented yet:
- real drawing generation
- real render generation
- manufacturing-fidelity detail for every mechanism
- tolerance-verified assembly interference / motion simulation

What is implemented now after the follow-up sessions:
- all files under `cad/components/` and `cad/assemblies/` now build
- `scripts/build_exports.py` now exports assemblies correctly via `assy.toCompound()`
- test coverage includes component tests, assembly smoke tests, pure-params assembly clearance checks, and CadQuery-backed geometric overlap checks
- the previously documented geometric overlap contracts now pass with current nominal geometry

### Important behavioral rule
The repo is no longer mostly stubs, but several solids remain **nominal V1 geometry**.
So:
- treat current CAD as exportable and testable
- do **not** overclaim manufacturing readiness where docs/components explicitly mark honest gaps

---

## 5. Must-read files for a new session

### In the repo
Read these first:
1. `CLAUDE.md`
2. `HANDOFF.md`
3. `README.md`
4. `cad/params.py`
5. `docs/design_spec.md`
6. `docs/manufacturability.md`
7. `docs/fmea.md`
8. `docs/toolchain_bluefin.md`
9. `docs/cadquery_modeling_plan.md`
10. `docs/repo_structure.md`

### Outside the repo (source artifacts from this session)
These were generated earlier and can still be useful reference:
- `/var/home/adrifadilah/Learns/coffee/filter_shaper_v1_spec.md`
- `/var/home/adrifadilah/Learns/coffee/manufacturability_v1.md`
- `/var/home/adrifadilah/Learns/coffee/filter-shaping-tool-brief.md`
- `/var/home/adrifadilah/Learns/coffee/cad-toolchain-bluefin.md`
- `/var/home/adrifadilah/Learns/coffee/cadquery_modeling_plan_v1.md`

---

## 6. CAD/environment decisions

### Platform
Host machine:
- **Bluefin 43** (Fedora Silverblue-like)
- system Python = **3.14**

### Important compatibility constraint
CadQuery/OCP path should use **Python 3.12**, not system 3.14.

### Correct local setup
```bash
cd /var/home/adrifadilah/Learns/coffee/conical-filter-shaper
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e '.[dev]'
```

### Tool choices
- **CadQuery** for modeling
- **FreeCAD** only as helper/viewer for now

### FreeCAD recommendation
Do not mutate the immutable host unnecessarily.
Prefer:
- **Flatpak** for GUI
- **AppImage extraction** for headless/CLI use

---

## 7. Key design decisions already made

### Product direction
This is **not** just an SD1R ruler clone.

It is intended to become a:
> **Universal Conical Filter Shaping System**

### V1 mechanism direction
Current chosen architecture:
- **indexed split-shell mandrel**
- ball detent indexing
- 48 / 60 / 80 degree presets

### Material direction
V1 direction from docs:
- shells: **POM-C**
- tip insert: **SS316L**
- ring / housing: **6061-T6 anodized**
- eject rod: **SS304 / SS316**

### Workflow direction
CadQuery models should be:
- parameter-driven
- modular by component
- assembled in `cad/assemblies/`
- validated by tests/scripts

### Commit policy
Commit:
- source
- docs
- tests
- scripts
- CSV BOM

Do not commit:
- generated exports
- renders
- local caches / venv artifacts

---

## 8. Important caveats / open issues

### A. Resolved paper/workflow direction
This was the biggest conceptual mismatch in the earlier scaffold, and it has now been resolved in the source-of-truth docs.

#### V1 now assumes:
- **standard pre-seamed conical paper filters**
- common **02-class** papers as the reference family
- **60° / P2** as the primary workflow target
- shell seam-relief + seam-guide handling, not raw-disc seam creation

#### V1 explicitly does NOT assume:
- **185 mm circular paper filter discs** as the user input
- disc-centric wrapping from a flat blank
- user-created seam overlap as the primary workflow

### Meaning
Future geometry work should follow the pre-seamed-paper workflow unless the product direction is explicitly changed again.

---

### B. 80° preset still needs real validation
80° is conceptually useful, but actual compatibility must be tested against:
- UFO-style workflows
- larger papers
- specific drippers

Do not overcommit to 80° in physical geometry or marketing until validated.

---

### C. `gen_drawings.py` and `render_all.py` are placeholders
They exist so the repo is internally consistent, but they do not generate real output yet.

That is intentional.

---

### D. FreeCAD is not installed/configured in repo yet
Only documentation exists for the recommended setup.

---

## 9. What was fixed in the repo during this session

### Packaging/tooling
- fixed `pyproject.toml` backend
- pinned Python compatibility to `<3.13`
- removed broken `cq-cli` dependency
- added `.python-version`

### Documentation
- fixed bad internal links
- added:
  - `docs/toolchain_bluefin.md`
  - `docs/cadquery_modeling_plan.md`
  - `docs/repo_structure.md`
- added `HANDOFF.md`

### Scripts
- added placeholder:
  - `scripts/gen_drawings.py`
  - `scripts/render_all.py`
- fixed `scripts/build_exports.py` assembly loop logic

### Tests / logic
- fixed cam geometry 180°-per-follower assumption
- made component tests skip gracefully when geometry is still stubbed
- fixed full test collection by adding `tests/__init__.py`
- normalized detent-dimple wording around **ball diameter** convention

### Cleanup
- removed local `__pycache__`, egg-info, pytest cache after validation

---

## 10. Recommended next steps

### Immediate next step (recommended)
Now that all current stubs are implemented, shift from scaffold build-out to **geometry quality and validation**.

### Recommended implementation order
1. improve shell geometry fidelity and reduce hardcoded helper tuning numbers
2. physically validate the updated tip-insert / ejection-stack behavior against paper handling
3. reconcile `docs/manufacturability.md` with the actual current mechanism
4. replace placeholder drawing/render scripts with real output generation
5. add motion- and tolerance-aware validation beyond the current nominal clearance checks

Why this order:
- the biggest remaining risks are correctness and manufacturability, not missing files
- the repo now benefits more from verification than from additional nominal geometry

---

## 11. Useful commands for the next session

### Activate environment
```bash
cd /var/home/adrifadilah/Learns/coffee/conical-filter-shaper
source .venv/bin/activate
```

### Run all tests
```bash
pytest tests -q
```

### Run geometry validation
```bash
python scripts/validate_geometry.py
```

### Generate BOM
```bash
python scripts/gen_bom.py
```

### Placeholder scripts
```bash
python scripts/gen_drawings.py
python scripts/render_all.py
```

---

## 12. Obsidian notes created in this session

Vault:
`/var/home/adrifadilah/Tooling/cognitive-vault`

Notes created under **`Everything Coffee/`**:
- `Universal Conical Filter Shaping Tool - V1 Mechanism.md`
- `Coffee Stall Plan 1.md`
- `SD1R Brewing Recipes.md`

Note: there are currently **two similar folders** in the vault:
- `Everything Coffee`
- `everything coffee`

This duplication was observed but not merged.

---

## 13. Quick summary for the next agent

If you only remember 5 things, remember these:

1. **Use Python 3.12**, not system 3.14.
2. **CadQuery is the source of truth.**
3. The repo now has nominal geometry for all current components and assemblies, but some mechanisms are still simplified.
4. V1 input paper is **standard pre-seamed cone paper**, not a flat circular disc.
5. Best next move is **validation/refinement**, not more stub-filling.
