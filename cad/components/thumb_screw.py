"""
Thumb Screw — Hinged V-Shape Filter Ruler
==========================================
M5 knurled thumb screw for positive angle lock of the ruler legs.

Provides manual tightening to lock the legs at the desired angle.
Used in combination with the magnetic friction hinge.

Dimensions
----------
- Head: Ø15mm knurled cylinder, 8mm height
- Shaft: M5 × 8mm threaded portion
- Material: SS304 stainless steel

Origin Convention
-----------------
- Origin at bottom of threaded shaft (engages with pivot bolt)
- +Z up through screw axis
- Head sits at top (+Z direction)

Qty: 1 per ruler

Usage
-----
    from cad.components.thumb_screw import build
    screw = build(params=p)  # -> cq.Workplane
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None) -> "cq.Workplane":
    """
    Build the thumb screw as a CadQuery Workplane solid.

    Parameters
    ----------
    params : module, optional
        Design parameter module (cad.params). Defaults to cad.params.

    Returns
    -------
    cq.Workplane
        Solid body of thumb screw (knurled head + threaded shaft).
    """
    if cq is None:
        raise ImportError("CadQuery is required for thumb_screw.build()")

    # Use provided params or default
    if params is None:
        import cad.params as params

    # Extract dimensions with defaults
    head_diameter = getattr(params, 'THUMB_SCREW_HEAD_DIAMETER_MM', 15.0)
    head_height = getattr(params, 'THUMB_SCREW_HEAD_HEIGHT_MM', 8.0)
    shaft_diameter = getattr(params, 'THUMB_SCREW_SHAFT_DIAMETER_MM', 5.0)
    shaft_length = getattr(params, 'THUMB_SCREW_SHAFT_LENGTH_MM', 8.0)
    knurl_count = getattr(params, 'THUMB_SCREW_KNURL_COUNT', 12)

    # Build knurled head
    # Main cylinder
    head = (
        cq.Workplane("XY")
        .circle(head_diameter / 2)
        .extrude(head_height)
    )
    
    # Add knurling texture as vertical ridges around perimeter
    # Create ridges by subtracting thin wedges
    ridge_depth = 0.3  # mm
    for i in range(knurl_count):
        angle = i * 360 / knurl_count
        # Create a thin vertical cutter
        cutter_width = head_diameter * 3.14159 / knurl_count * 0.3
        cutter = (
            cq.Workplane("XY")
            .box(cutter_width, ridge_depth, head_height + 0.1, centered=True)
            .translate((head_diameter/2 + ridge_depth/2, 0, head_height/2))
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        head = head - cutter

    # Add top chamfer for aesthetics
    chamfer_size = 1.0
    try:
        head = head.faces(">Z").chamfer(chamfer_size)
    except Exception:
        pass  # Chamfer may fail, skip if so

    # Build threaded shaft
    shaft = (
        cq.Workplane("XY")
        .circle(shaft_diameter / 2)
        .extrude(shaft_length)
        .translate((0, 0, -shaft_length))  # Shaft extends downward from origin
    )

    # Combine head and shaft
    screw = head + shaft

    return screw
