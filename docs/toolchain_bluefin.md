# AI-Agent-Friendly Linux CAD Toolchain

Target environment:
- **Bluefin 43 / Fedora Silverblue-style immutable host**
- `uv` installed
- system Python may be newer than CadQuery supports

---

## Opinionated recommendation

Use this stack:

- **CadQuery** = source of truth for geometry
- **FreeCAD** = viewer / checker / optional drawings
- **uv + Python 3.12** = cleanest agent-friendly setup
- **FreeCAD Flatpak or extracted AppImage** = best fit for immutable Linux

---

## Important compatibility note

CadQuery/OCP wheels are not reliable on Python 3.14 in this environment.

### Use Python 3.12

```bash
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The repo includes:

```text
.python-version = 3.12
```

---

## CadQuery setup

### Why CadQuery
- fully headless
- Python-native
- easy for AI agents to edit
- deterministic in git
- ideal for parametric products with preset angles and tolerances

### Install

```bash
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Verify

```bash
python -c "import cadquery as cq; print(cq.Workplane('XY').box(1,2,3).val().BoundingBox().xlen)"
```

---

## FreeCAD setup

## GUI option: Flatpak

```bash
flatpak install flathub org.freecadweb.FreeCAD
flatpak run org.freecadweb.FreeCAD
```

Use this for:
- viewing STEP files
- checking assemblies visually
- occasional manual inspection

## Headless option: AppImage extraction

```bash
curl -LO https://github.com/FreeCAD/FreeCAD/releases/download/1.1.0/FreeCAD_1.1.0-Linux-x86_64-py311.AppImage
chmod +x FreeCAD_1.1.0-Linux-x86_64-py311.AppImage
./FreeCAD_1.1.0-Linux-x86_64-py311.AppImage --appimage-extract
```

Then use:

```bash
squashfs-root/usr/bin/FreeCADCmd
```

Use this for:
- headless FreeCAD scripts
- STEP import/export checks
- non-GUI automation

---

## Why not rpm-ostree install?

Avoid layering FreeCAD into the immutable host unless absolutely necessary.

Prefer:
- **Flatpak** for GUI
- **AppImage** for headless use
- **uv venv** for CadQuery

---

## Best export formats

Use:
- **STEP** → main interchange format
- **STL** → print prototypes
- **DXF / SVG** → 2D cut profiles and documentation

---

## Recommended workflow

### Human + agent workflow
1. model in **CadQuery**
2. export **STEP**
3. inspect in **FreeCAD**
4. prototype via STL / CNC handoff via STEP

### Why this is best
- Linux-native
- agent-friendly
- scriptable
- works cleanly with git
- avoids GUI-only CAD traps

---

## Optional containerized path

If you want stronger isolation on Bluefin, use `distrobox` or `toolbx`.

That is useful if you want:
- multiple CAD tool versions
- a disposable environment
- extra FreeCAD/CAD dependencies without touching host state

But for this repo, **uv + Python 3.12 + FreeCAD Flatpak/AppImage** is the preferred default.
