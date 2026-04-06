"""
PTFE Slide Strip — Universal Filter Ruler
==========================================
Optional low-friction liner for the T-slot rail, reducing stick-slip during
arm adjustment and improving feel at the angle scale.
  - Material: PTFE, 0.5mm thick
  - Installed in the T-slot rail undercut channel
  - Press-fit or adhesive-backed

Qty per assembly: 2 (one per rail/arm)
Spec ref: docs/design_spec.md § T-Slot Rails (PTFE Insert note)

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
    PTFE_LENGTH_MM,
    PTFE_WIDTH_MM,
    PTFE_THICKNESS_MM,
)


def build(params=None) -> "cq.Workplane":
    """
    Build PTFE slide strip solid.

    Parameters
    ----------
    params : module, optional
        The cad.params module (for consistent parameter access). If None,
        constants are imported directly.

    Returns
    -------
    cq.Workplane
        A CadQuery workplane containing the PTFE strip solid.

    Geometry
    --------
    - Simple rectangular strip: 180mm × 6mm × 0.5mm
    - Origin at center of bottom face
    - Designed to press-fit into T-slot rail undercut
    """
    if cq is None:
        raise ImportError("CadQuery is required for ptfe_slide_strip.build()")

    # Use params if provided, otherwise use imported constants
    if params is not None:
        length = params.PTFE_LENGTH_MM
        width = params.PTFE_WIDTH_MM
        thickness = params.PTFE_THICKNESS_MM
    else:
        length = PTFE_LENGTH_MM
        width = PTFE_WIDTH_MM
        thickness = PTFE_THICKNESS_MM

    # ── Simple rectangular strip ─────────────────────────────────────────────
    # Box centered on origin at bottom face

    strip = (
        cq.Workplane("XY")
        .box(length, width, thickness, centered=(True, True, False))
    )

    # PTFE is very soft, no edge breaks needed
    # Strip is pressed into T-slot undercut

    return strip


def build_assembly(params=None) -> "cq.Workplane":
    """
    Build PTFE strip assembly (strip only).

    Returns
    -------
    cq.Workplane
        The PTFE strip assembly.
    """
    if cq is None:
        raise ImportError("CadQuery is required for ptfe_slide_strip.build_assembly()")

    return build(params=params)