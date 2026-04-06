"""
Cam Lock — Universal Filter Ruler
====================================
Eccentric cam mechanism that clamps the sliding arm in position.
  - 90° throw, single-handed operation
  - Cam body: SS 316, eccentric pivot
  - Lever: 6061-T6 Al, 25mm, knurled end
  - Mounting: M5 shoulder bolt into base plate
  - Clamping force: ≥50 N

Qty per assembly: 2 (one per arm)
Spec ref: docs/design_spec.md § Cam Lock Mechanism

Coordinate System
-----------------
- Origin: Center of cam disc (rotation axis)
- X-axis: Horizontal (lever points in +X when unlocked)
- Y-axis: Perpendicular to lever
- Z-axis: Rotation axis (cam disc plane is XY)
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

from cad.params import (
    CAM_LEVER_LENGTH_MM,
    CAM_THROW_DEG,
)


# Cam lock geometry constants
CAM_DISC_DIAMETER_MM = 12.0          # Eccentric cam disc outer diameter
CAM_DISC_THICKNESS_MM = 6.0         # Cam disc thickness
CAM_LOCK_ECCENTRICITY_MM = 2.0      # Distance from center to pivot (offset)
CAM_LEVER_WIDTH_MM = 8.0            # Width of lever arm (perpendicular to length)
CAM_M5_BORE_MM = 5.4                # M5 clearance hole (slightly oversized)
CAM_M5_BORE_DEPTH_MM = 10.0         # Bore depth through cam center


def build(params=None) -> "cq.Workplane":
    """
    Build cam lock body solid with eccentric cam disc and lever arm.

    Parameters
    ----------
    params : module, optional
        The cad.params module (for consistent parameter access). If None,
        constants are imported directly.

    Returns
    -------
    cq.Workplane
        A CadQuery workplane containing the cam lock solid.

    Geometry
    --------
    - Eccentric cam disc: 12mm OD, centered at origin
    - Pivot offset: 2mm eccentricity (offset hole for M5 bolt)
    - Lever arm: 25mm long × 8mm wide, attached to cam disc
    - M5 bore through center (for shoulder bolt)
    - 90° throw rotation from unlock to lock position
    """
    if cq is None:
        raise ImportError("CadQuery is required for cam_lock.build()")

    # Use params if provided, otherwise use imported constants
    if params is not None:
        lever_length = params.CAM_LEVER_LENGTH_MM
        throw_deg = params.CAM_THROW_DEG
    else:
        lever_length = CAM_LEVER_LENGTH_MM
        throw_deg = CAM_THROW_DEG

    # ── Cam disc ──────────────────────────────────────────────────────────────
    # Eccentric cam disc: 12mm OD, centered at origin
    # The eccentricity means the pivot hole is offset from geometric center

    cam_disc = (
        cq.Workplane("XY")
        .circle(CAM_DISC_DIAMETER_MM / 2)
        .extrude(CAM_DISC_THICKNESS_MM)
    )

    # ── Lever arm ─────────────────────────────────────────────────────────────
    # Lever extends from cam disc edge
    # Width is perpendicular to lever direction

    # Lever profile starts at edge of cam disc
    lever_start_x = CAM_DISC_DIAMETER_MM / 2

    lever_profile = (
        cq.Workplane("XY")
        .moveTo(lever_start_x, -CAM_LEVER_WIDTH_MM / 2)
        .lineTo(lever_start_x + lever_length, -CAM_LEVER_WIDTH_MM / 2)
        .lineTo(lever_start_x + lever_length, CAM_LEVER_WIDTH_MM / 2)
        .lineTo(lever_start_x, CAM_LEVER_WIDTH_MM / 2)
        .close()
    )

    lever = lever_profile.extrude(CAM_DISC_THICKNESS_MM)

    # Union cam disc and lever
    cam_lock = cam_disc.union(lever)

    # ── Eccentric pivot hole ──────────────────────────────────────────────────
    # M5 clearance hole offset from center by eccentricity amount
    # When cam rotates, this offset causes clamping action

    pivot_hole = (
        cq.Workplane("XY")
        .circle(CAM_M5_BORE_MM / 2)
        .extrude(CAM_DISC_THICKNESS_MM * 2)  # Through hole
        .translate((-CAM_LOCK_ECCENTRICITY_MM, 0, 0))  # Offset from center
    )

    cam_lock = cam_lock.cut(pivot_hole)

    # ── Edge fillets ──────────────────────────────────────────────────────────
    # R1mm fillets on lever edges for comfort

    try:
        cam_lock = cam_lock.edges("|Z").fillet(1.0)
    except Exception:
        pass  # Skip fillet if it fails

    return cam_lock


def build_assembly(params=None) -> "cq.Workplane":
    """
    Build cam lock assembly (cam disc + lever as single solid).

    Returns
    -------
    cq.Workplane
        The cam lock assembly.
    """
    if cq is None:
        raise ImportError("CadQuery is required for cam_lock.build_assembly()")

    return build(params=params)