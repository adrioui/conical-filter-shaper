"""
Ferrous Track Strip — Universal Filter Ruler
==============================================
Mild steel strip recessed into the base plate top surface;
provides the magnetic attraction surface for the magnetic markers.
  - Dimensions: 180mm × 6mm × 1mm
  - Material: Mild steel, zinc plated
  - Recess depth into base plate: 1mm
  - Adhesive-mounted (or press-fit in recess)

Qty per assembly: 1
Spec ref: docs/design_spec.md § Magnetic Track

Coordinate System
-----------------
- Origin: Center of bottom face
- X-axis: Length (180mm)
- Y-axis: Width (6mm)
- Z-axis: Up (top face at +Z)
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

from cad.params import (
    MARKER_TRACK_LENGTH_MM,
    PTFE_WIDTH_MM,  # Same width as PTFE strip (6mm)
    MARKER_TRACK_RECESS_DEPTH_MM,
)


# Ferrous strip dimensions (mild steel strip)
FERROUS_STRIP_LENGTH_MM = MARKER_TRACK_LENGTH_MM  # 180mm (from params)
FERROUS_STRIP_WIDTH_MM = PTFE_WIDTH_MM            # 6mm (same as PTFE)
FERROUS_STRIP_THICKNESS_MM = 1.0                  # 1mm thick


def build(params=None) -> "cq.Workplane":
    """
    Build ferrous strip solid.

    Parameters
    ----------
    params : module, optional
        The cad.params module (for consistent parameter access). If None,
        constants are imported directly.

    Returns
    -------
    cq.Workplane
        A CadQuery workplane containing the ferrous strip solid.

    Geometry
    --------
    - Simple rectangular bar: 180mm × 6mm × 1mm
    - Origin at center of bottom face
    - Designed to be recessed 1mm into base plate
    """
    if cq is None:
        raise ImportError("CadQuery is required for ferrous_strip.build()")

    # Use params if provided, otherwise use imported constants
    if params is not None:
        length = params.MARKER_TRACK_LENGTH_MM
        width = params.PTFE_WIDTH_MM
        thickness = FERROUS_STRIP_THICKNESS_MM
    else:
        length = FERROUS_STRIP_LENGTH_MM
        width = FERROUS_STRIP_WIDTH_MM
        thickness = FERROUS_STRIP_THICKNESS_MM

    # ── Simple rectangular strip ─────────────────────────────────────────────
    # Box centered on origin at bottom face

    strip = (
        cq.Workplane("XY")
        .box(length, width, thickness, centered=(True, True, False))
    )

    # ── Edge breaks ──────────────────────────────────────────────────────────
    # Small chamfer on edges to prevent sharp corners
    # (0.2mm break is typical for sheet metal)

    try:
        # Fillet all edges with small radius
        strip = strip.edges("|Z").fillet(0.15)
    except Exception:
        pass  # Skip if fillet fails

    return strip


def build_assembly(params=None) -> "cq.Workplane":
    """
    Build ferrous strip assembly (strip only, no hardware).

    Returns
    -------
    cq.Workplane
        The ferrous strip assembly.
    """
    if cq is None:
        raise ImportError("CadQuery is required for ferrous_strip.build_assembly()")

    return build(params=params)