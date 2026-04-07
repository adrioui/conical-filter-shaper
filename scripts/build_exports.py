#!/usr/bin/env python3
"""
Build all CAD exports: STEP, STL, SVG, DXF.

Bevel Gauge with Tapered Arms — Revision r3-0
==============================================
Components: ruler_arm, pivot_hinge, thumb_screw
Assemblies: ruler_assy (at 60 degree default angle)
Revision:  r3-0 (tapered arm design, bevel gauge style)

Usage:
    python scripts/build_exports.py [--angle 60] [--formats step stl svg dxf]

Output:
    exports/step/components/{part}_r2-0.step
    exports/step/assemblies/{assy}_assy_r2-0.step
    exports/stl/components/{part}_r2-0.stl
    exports/svg/components/{part}_section_r2-0.svg
    exports/dxf/components/{part}_r2-0.dxf   (2D-profile parts only)

All outputs are gitignored — commit the source in cad/, not the exports.
"""
from __future__ import annotations
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

try:
    import cadquery as cq
except ImportError:
    print("ERROR: CadQuery not installed. Run: pip install cadquery")
    sys.exit(1)

import typer
from rich.console import Console
from rich.progress import track
import cad.params as P

app = typer.Typer(help=__doc__)
console = Console()

# Hinged V-Shape Filter Ruler components (r2-0)
COMPONENT_MODULES = [
    "ruler_arm",
    "pivot_hinge",
    "thumb_screw",
]

# Hinged V-Shape Filter Ruler assemblies (r2-0)
ASSEMBLY_MODULES = [
    "ruler_assy",
]

# Parts that also export a DXF 2D profile (flat/2D parts)
# None of the r2-0 components are flat-profile DXF parts
DXF_PARTS: set = set()


def export_dir(fmt: str, kind: str) -> Path:
    d = ROOT / "exports" / fmt / kind
    d.mkdir(parents=True, exist_ok=True)
    return d


def rev_slug() -> str:
    """Revision slug: r{major}-{minor}."""
    return f"r{P.REVISION.replace('.', '-')}"


@app.command()
def main(
    angle: float = typer.Option(60.0, help="Angle in degrees for ruler_assy (40-85)"),
    formats: list[str] = typer.Option(["step", "stl", "svg", "dxf"], help="Formats to export"),
):
    rev = rev_slug()
    console.rule(f"[bold]Building exports — hinged V-shape ruler rev {P.REVISION} (r{rev})[/bold]")

    # ── Components ────────────────────────────────────────────────────────────
    console.print("\n[cyan]Components[/cyan]")
    for mod_name in track(COMPONENT_MODULES, description="Exporting components..."):
        try:
            mod = importlib.import_module(f"cad.components.{mod_name}")

            # ruler_arm needs side parameter for build
            if mod_name == "ruler_arm":
                shape = mod.build(params=P, side="left")
            else:
                shape = mod.build(params=P)

            for fmt in formats:
                if fmt == "step":
                    out = export_dir("step", "components") / f"{mod_name}_{rev}.step"
                    cq.exporters.export(shape, str(out))
                    console.print(f"  ✅ {mod_name}_{rev}.step")
                elif fmt == "stl":
                    out = export_dir("stl", "components") / f"{mod_name}_{rev}.stl"
                    cq.exporters.export(shape, str(out))
                    console.print(f"  ✅ {mod_name}_{rev}.stl")
                elif fmt == "svg":
                    out = export_dir("svg", "components") / f"{mod_name}_section_{rev}.svg"
                    cq.exporters.export(shape, str(out), opt={"projectionDir": (0, 1, 0)})
                    console.print(f"  ✅ {mod_name}_section_{rev}.svg")
                elif fmt == "dxf" and mod_name in DXF_PARTS:
                    out = export_dir("dxf", "components") / f"{mod_name}_{rev}.dxf"
                    cq.exporters.export(shape, str(out))

            console.print(f"  ✅ {mod_name}")
        except NotImplementedError:
            console.print(f"  ⚠️  {mod_name} — stub, skipped")
        except Exception as e:
            console.print(f"  ❌ {mod_name} — {e}")

    # ── Assemblies ────────────────────────────────────────────────────────────
    console.print("\n[cyan]Assemblies[/cyan]")
    for mod_name in track(ASSEMBLY_MODULES, description="Exporting assemblies..."):
        try:
            mod = importlib.import_module(f"cad.assemblies.{mod_name}")
            # ruler_assy accepts angle_deg parameter
            if mod_name == "ruler_assy":
                assy = mod.build(params=P, angle_deg=angle)
            else:
                assy = mod.build(params=P)

            assy_slug = f"{mod_name}_assy_{rev}"
            if "step" in formats:
                out = export_dir("step", "assemblies") / f"{assy_slug}.step"
                cq.exporters.export(assy.toCompound(), str(out))
                console.print(f"  ✅ {assy_slug}.step")
            if "stl" in formats:
                out = export_dir("stl", "assemblies") / f"{assy_slug}.stl"
                cq.exporters.export(assy.toCompound(), str(out))
                console.print(f"  ✅ {assy_slug}.stl")
            console.print(f"  ✅ {mod_name}")
        except NotImplementedError:
            console.print(f"  ⚠️  {mod_name} — stub, skipped")
        except Exception as e:
            console.print(f"  ❌ {mod_name} — {e}")

    console.rule("[green]Done[/green]")
    console.print(f"\n  Revision: {rev}")
    console.print(f"  Angle: {angle}°")
    console.print(f"  Formats: {', '.join(formats)}")


if __name__ == "__main__":
    app()
