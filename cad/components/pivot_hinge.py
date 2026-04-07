"""
Pivot Hinge — Hinged V-Shape Filter Ruler
==========================================
Friction hinge joining the two ruler arms at the pivot point.

Components (v3.0 — no magnet, friction-only pivot)
--------------------------------------------------
- M5 shoulder bolt (pivot axle)
- PTFE washer: 0.5mm thick (between arms for smooth rotation)

The thumb screw (separate component) provides positive locking.

Dimensions (from params.py)
---------------------------
- Shoulder bolt head: 10mm diameter × 3mm height
- Shoulder: 8mm diameter × 4mm length
- Thread: M5 (5mm diameter) × 6mm length
- PTFE washer: 10mm OD × 5.3mm ID × 0.5mm thick

Origin Convention
-----------------
- Origin at bolt center axis (Z=0)
- +Z upward (bolt head side)
- -Z downward (thread side)

Qty: 1 per ruler

Usage
-----
    from cad.components.pivot_hinge import build
    hinge = build()  # -> cq.Workplane

    from cad.components.pivot_hinge import build
    hinge = build(params=p)  # -> cq.Workplane
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None) -> "cq.Workplane":
    """
    Build the pivot hinge as a combined CadQuery Workplane.

    The hinge consists of (v3.0 — no magnet):
    - Shoulder bolt (vertical through arms)
    - PTFE washer (between bolt head and top arm)

    All parts are combined into a single solid for export.

    Parameters
    ----------
    params : module, optional
        Design parameter module (cad.params). Defaults to cad.params.

    Returns
    -------
    cq.Workplane
        Combined solid containing bolt and washer.
    """
    if cq is None:
        raise ImportError("CadQuery is required for pivot_hinge.build()")

    # Use provided params or default
    if params is None:
        import cad.params as params

    # === PIVOT HARDWARE PARAMETERS ===
    # Bolt dimensions
    head_diameter = getattr(params, 'PIVOT_BOLT_HEAD_DIA_MM', 10.0)
    head_height = getattr(params, 'PIVOT_BOLT_HEAD_HEIGHT_MM', 3.0)
    shoulder_diameter = getattr(params, 'PIVOT_SHOULDER_DIAMETER_MM', 8.0)
    shoulder_length = getattr(params, 'PIVOT_SHOULDER_LENGTH_MM', 4.0)
    thread_diameter = getattr(params, 'PIVOT_BOLT_DIAMETER_MM', 5.0)
    thread_length = 6.0

    # Washer dimensions
    washer_od = getattr(params, 'WASHER_OD_MM', 10.0)
    washer_id = getattr(params, 'WASHER_ID_MM', 5.3)
    washer_thickness = getattr(params, 'WASHER_THICKNESS_MM', 0.5)

    # === BUILD SHOULDER BOLT ===
    # Stack vertically: head on top (+Z), shoulder in middle, thread at bottom (-Z)

    # Bolt head (cylinder at top, +Z direction)
    bolt_head = (
        cq.Workplane("XY")
        .circle(head_diameter / 2)
        .extrude(head_height)
    )

    # Shoulder (smooth section, between head and thread)
    shoulder = (
        cq.Workplane("XY")
        .circle(shoulder_diameter / 2)
        .extrude(shoulder_length)
        .translate((0, 0, head_height))  # Position below head
    )

    # Thread (below shoulder, extends into -Z)
    thread = (
        cq.Workplane("XY")
        .circle(thread_diameter / 2)
        .extrude(thread_length)
        .translate((0, 0, head_height + shoulder_length))  # Position below shoulder
    )

    # Combine bolt parts — origin at Z=0 (center of shoulder/bolt assembly)
    bolt = bolt_head + shoulder + thread

    # === BUILD PTFE WASHER ===
    # Ring shape between the two arms in assembly
    washer = (
        cq.Workplane("XY")
        .circle(washer_od / 2)
        .extrude(washer_thickness)
    )
    # Cut center hole for shoulder bolt
    washer = washer.faces(">Z").workplane().hole(washer_id)

    # Position washer: centered at Z=0 (between arms, around shoulder)
    # In the assembly, the washer sits around the shoulder section
    washer_positioned = washer.translate((0, 0, 0))

    # === COMBINE INTO SINGLE WORKPLANE ===
    # All centered on Z axis at origin
    combined = bolt + washer_positioned

    return combined