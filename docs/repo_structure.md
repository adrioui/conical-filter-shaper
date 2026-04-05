# Repository Structure

Annotated structure for `conical-filter-shaper`.

---

## Top level

```text
conical-filter-shaper/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── .python-version
├── .gitignore
├── cad/
├── tests/
├── scripts/
├── docs/
├── manufacturing/
├── refs/
├── exports/   # generated, gitignored
└── renders/   # generated, gitignored
```

---

## `cad/` — source of truth

```text
cad/
├── params.py
├── components/
├── assemblies/
└── utils/
```

### Rules
- commit everything in `cad/`
- no magic numbers in component files
- all key dimensions come from `cad/params.py`

---

## `tests/`

Contains:
- pure math checks
- parameter consistency checks
- geometry smoke tests
- assembly validation tests

Commit all of it.

---

## `scripts/`

Utility scripts for:
- export generation
- geometry validation
- BOM generation
- revision bumping
- future drawing/render automation

Scripts may exist as stubs before full geometry implementation lands.

---

## `docs/`

Human-facing design documentation:
- design spec
- manufacturability
- FMEA
- ADRs
- Linux CAD toolchain notes
- CadQuery implementation plan
- repo structure

---

## `manufacturing/`

Vendor handoff material:
- committed CSV BOM
- inspection docs
- surface finish notes
- generated drawings folder

Only source docs and CSV should be committed.
Generated PDFs/DXFs/XLSX stay gitignored.

---

## `refs/`

Reference material:
- dripper dimensions
- filter specs
- competitor notes
- standards

Small text files are ideal. Large binaries should use Git LFS if needed.

---

## `exports/` and `renders/`

Generated only.
Never edit manually.
Never treat as source-of-truth.

Typical contents:
- `exports/step/`
- `exports/stl/`
- `exports/svg/`
- `exports/dxf/`
- `renders/components/`
- `renders/assembly/`

---

## Naming conventions

### Python source
- `snake_case.py`

### Export files
- `{part_name}_r0-1.step`
- `{assembly_name}_assy_r0-1.step`

### Parameters
- `UPPER_SNAKE_CASE_MM`
- `*_DEG`
- `*_UM`
- `*_N`

---

## Commit policy

### Commit
- CAD source
- tests
- scripts
- markdown docs
- CSV BOM

### Do not commit
- generated STEP/STL files
- generated drawings
- generated renders
- temporary viewer/session files
- local venv files
