#!/usr/bin/env python3
"""
Build all CAD exports: STEP, STL, SVG, DXF.

Usage:
    python scripts/build_exports.py [--preset P1|P2|P3|all] [--formats step stl svg dxf]

Output:
    exports/step/components/{part}_r{rev}.step
    exports/step/assemblies/{assy}_assy_r{rev}.step
    exports/stl/components/{part}_r{rev}.stl
    exports/svg/components/{part}_section_r{rev}.svg
    exports/dxf/components/{part}_r{rev}.dxf   (2D-profile parts only: overlap_fin for now)

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


COMPONENT_MODULES = [
    "shell_half_l",
    "shell_half_r",
    "tip_insert_block",
    "cam_ring",
    "handle_housing",
    "handle_grip_insert",
    "overlap_fin",
    "ejection_rod",
    "base_cap",
]

ASSEMBLY_MODULES = [
    "mandrel_assy",
    "ring_assy",
    "ejection_assy",
    "full_assy",
]

# Parts that also export a DXF 2D profile
DXF_PARTS = {"overlap_fin"}


def export_dir(fmt: str, kind: str) -> Path:
    d = ROOT / "exports" / fmt / kind
    d.mkdir(parents=True, exist_ok=True)
    return d


def rev_slug() -> str:
    return f"r{P.REVISION.replace('.', '-')}"


@app.command()
def main(
    preset: str = typer.Option("all", help="Preset to use for assemblies: P1/P2/P3/all"),
    formats: list[str] = typer.Option(["step", "stl", "svg", "dxf"], help="Formats to export"),
):
    rev = rev_slug()
    console.rule(f"[bold]Building exports — rev {P.REVISION}[/bold]")

    # ── Components ────────────────────────────────────────────────────────────
    console.print("\n[cyan]Components[/cyan]")
    for mod_name in track(COMPONENT_MODULES, description="Exporting components..."):
        try:
            mod = importlib.import_module(f"cad.components.{mod_name}")
            shape = mod.build()

            for fmt in formats:
                if fmt == "step":
                    out = export_dir("step", "components") / f"{mod_name}_{rev}.step"
                    cq.exporters.export(shape, str(out))
                elif fmt == "stl":
                    out = export_dir("stl", "components") / f"{mod_name}_{rev}.stl"
                    cq.exporters.export(shape, str(out))
                elif fmt == "svg":
                    out = export_dir("svg", "components") / f"{mod_name}_section_{rev}.svg"
                    cq.exporters.export(shape, str(out), opt={"projectionDir": (0, 1, 0)})
                elif fmt == "dxf" and mod_name in DXF_PARTS:
                    out = export_dir("dxf", "components") / f"{mod_name}_{rev}.dxf"
                    cq.exporters.export(shape, str(out))

            console.print(f"  ✅ {mod_name}")
        except NotImplementedError:
            console.print(f"  ⚠️  {mod_name} — stub, skipped")
        except Exception as e:
            console.print(f"  ❌ {mod_name} — {e}")

    # ── Assemblies ────────────────────────────────────────────────────────────
    presets_to_export = P.PRESETS if preset == "all" else [
        next(p for p in P.PRESETS if p.label == preset)
    ]

    console.print("\n[cyan]Assemblies[/cyan]")
    for mod_name in ASSEMBLY_MODULES:
        mod = importlib.import_module(f"cad.assemblies.{mod_name}")
        preset_iter = [None] if mod_name == "ejection_assy" else presets_to_export
        for p in preset_iter:
            label = p.label if p is not None else "base"
            try:
                assy = mod.build(preset=p) if p is not None else mod.build()

                assy_slug = (
                    f"{mod_name}_{label.lower()}_{rev}"
                    if preset == "all" and p is not None
                    else f"{mod_name}_{rev}"
                )
                if "step" in formats:
                    out = export_dir("step", "assemblies") / f"{assy_slug}.step"
                    cq.exporters.export(assy.toCompound(), str(out))
                console.print(f"  ✅ {mod_name} ({label})")
            except NotImplementedError:
                console.print(f"  ⚠️  {mod_name} ({label}) — stub, skipped")
            except Exception as e:
                console.print(f"  ❌ {mod_name} ({label}) — {e}")

    console.rule("[green]Done[/green]")


if __name__ == "__main__":
    app()
