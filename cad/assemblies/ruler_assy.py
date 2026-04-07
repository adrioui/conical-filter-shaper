"""
Ruler Assembly — Hinged V-Shape Filter Ruler
=============================================
Top-level assembly: two ruler arms + pivot hinge + PTFE washer + thumb screw.

The two SS304 tapered arms are joined at one end by the friction pivot hinge.
A thumb screw provides positive angle lock. The assembly opens to any angle
from 40° to 85° and folds flat for pocket carry.

Sub-components:
  - ruler_arm (×2, left and right — identical parts)
  - pivot_hinge (×1, shoulder bolt + PTFE washer)
  - thumb_screw (×1, M5 knurled angle lock)

Origin: Pivot center at (0, 0, 0), +Z up through pivot axis.
Arms extend in ±X/Y plane based on angle_deg.

Usage
-----
    from cad.assemblies.ruler_assy import build
    assembly = build(angle_deg=60.0)  # -> cq.Assembly
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

from cad.utils.ruler_math import ANGLE_RANGE_MIN_DEG, ANGLE_RANGE_MAX_DEG


def build(
    params=None,
    angle_deg: float = 60.0,
) -> "cq.Assembly":
    """
    Build the full hinged ruler assembly at a given opening angle.

    Parameters
    ----------
    params : module, optional
        Design parameter module. Defaults to cad.params.
    angle_deg : float
        Full included angle between the two arm inner edges (degrees).
        Valid range: 40.0–85.0. Defaults to 60.0.

    Returns
    -------
    cq.Assembly
        Assembly containing:
          - "arm_bottom": bottom ruler arm (at Z=0)
          - "washer": PTFE washer (at Z=ARM_THICKNESS)
          - "arm_top": top ruler arm (at Z=ARM_THICKNESS + WASHER_THICKNESS)
          - "pivot_hinge": shoulder bolt at origin
          - "thumb_screw": M5 knurled lock screw on top of stack

    Raises
    ------
    ValueError
        If angle_deg is outside the operating range (40°–85°).
    """
    # Validate angle range
    if angle_deg < ANGLE_RANGE_MIN_DEG or angle_deg > ANGLE_RANGE_MAX_DEG:
        raise ValueError(
            f"angle_deg must be between {ANGLE_RANGE_MIN_DEG} and "
            f"{ANGLE_RANGE_MAX_DEG}, got {angle_deg}"
        )

    if cq is None:
        raise ImportError("CadQuery is required for ruler_assy.build()")

    # Use provided params or default
    if params is None:
        import cad.params as params

    # Import sub-components
    from cad.components.ruler_arm import build as build_arm
    from cad.components.pivot_hinge import build as build_hinge
    from cad.components.thumb_screw import build as build_screw

    # Get dimensions from params
    arm_thickness = params.ARM_THICKNESS_MM
    washer_thickness = params.WASHER_THICKNESS_MM

    # Build each component
    arm_bottom = build_arm(side="left")
    arm_top = build_arm(side="right")
    pivot_hinge = build_hinge(params=params)
    thumb_screw = build_screw(params=params)

    # Create assembly
    assembly = cq.Assembly(name="hinged_ruler")

    # Calculate half angle for arm rotation
    half_angle = angle_deg / 2.0

    # Stack heights:
    # - Bottom arm: bottom face at Z=0, top face at Z=ARM_THICKNESS
    # - Washer: at Z=ARM_THICKNESS (sits on bottom arm)
    # - Top arm: at Z=ARM_THICKNESS + WASHER_THICKNESS (sits on washer)
    #
    # The arm is centered on Z when built, so we need to offset it
    # Arm built has center at Z=0, so bottom face is at -ARM_THICKNESS/2
    # We want bottom face at Z=0, so translate by +ARM_THICKNESS/2

    # Bottom arm: rotated -half_angle, bottom face at Z=0
    bottom_arm_z = arm_thickness / 2
    assembly.add(
        arm_bottom,
        name="arm_bottom",
        loc=cq.Location(
            (0, 0, bottom_arm_z),
            (0, 0, 1),
            -half_angle  # Rotate -half_angle around Z axis
        )
    )

    # PTFE washer: at Z=ARM_THICKNESS (sits on top of bottom arm)
    # Build washer: OD=10mm, ID=5.3mm (M5 clearance)
    from cad.params import WASHER_OD_MM, WASHER_ID_MM, WASHER_THICKNESS_MM
    washer_z = arm_thickness + washer_thickness / 2
    washer = (
        cq.Workplane("XY")
        .circle(WASHER_OD_MM / 2)
        .extrude(WASHER_THICKNESS_MM)
    )
    washer = washer.faces(">Z").workplane().hole(WASHER_ID_MM)
    washer = washer.translate((0, 0, washer_z))
    assembly.add(washer, name="washer")

    # Top arm: at Z=ARM_THICKNESS + WASHER_THICKNESS, rotated +half_angle
    top_arm_z = arm_thickness + washer_thickness + arm_thickness / 2
    assembly.add(
        arm_top,
        name="arm_top",
        loc=cq.Location(
            (0, 0, top_arm_z),
            (0, 0, 1),
            half_angle  # Rotate +half_angle around Z axis
        )
    )

    # Pivot hinge (bolt) at origin, extending through the stack in Z
    assembly.add(pivot_hinge, name="pivot_hinge")

    # Thumb screw on top of stack
    # Top arm's top face is at: top_arm_z + ARM_THICKNESS/2
    # = arm_thickness + washer_thickness + arm_thickness = 2*arm_thickness + washer_thickness
    thumb_screw_z = arm_thickness + washer_thickness + arm_thickness + thumb_screw.val().BoundingBox().zmin * -1
    assembly.add(
        thumb_screw,
        name="thumb_screw",
        loc=cq.Location((0, 0, thumb_screw_z))
    )

    return assembly
