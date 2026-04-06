"""
Arm Assembly — Universal Filter Ruler
======================================
One sliding arm with its cam lock installed and PTFE slide strip.

Sub-components:
  - sliding_arm  (the aluminum arm body)
  - cam_lock     (eccentric cam + lever)
  - ptfe_strip   (low-friction liner for T-slot)

Sub-assemblies:
  - None

Origin: At the arm's pivot point (where cam lock engages).
        +Z up (arm body extends in +X direction).
        The T-slot tongue is on the bottom face (−Z).

Coordinate System
-----------------
- Origin: Pivot end of arm (cam lock hole end)
- X-axis: Along arm length (extends away from pivot)
- Y-axis: Lateral (fold guide on +Y side for left arm, -Y for right)
- Z-axis: Up (top face at +Z)

Usage
-----
    import cad.assemblies.arm_assy as arm_assy
    assembly = arm_assy.build(side="left")  # cq.Assembly
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params
from cad.components import sliding_arm, cam_lock, ptfe_slide_strip
from cad.utils.ruler_math import pivot_position


# Cam lock positioning relative to arm pivot hole
CAM_SLOT_CENTER_X_MM = 12.0  # Distance from pivot end to cam slot center (from params)
ARM_PIVOT_OFFSET_MM = 0.0   # Cam locked flush with arm top surface


def build(
    params=None,
    side: str = "left",
) -> "cq.Assembly":
    """
    Build one arm assembly (sliding arm + cam lock + PTFE strip).

    Parameters
    ----------
    params : module, optional
        Design parameter module. Defaults to cad.params.
    side : str
        Which arm: "left" or "right". Determines arm orientation.
        The PTFE strip is always positioned on the T-slot tongue (bottom face).

    Returns
    -------
    cq.Assembly
        Assembly containing the named parts:
          - "arm": sliding_arm solid
          - "cam_lock": cam lock mechanism
          - "ptfe_strip": PTFE slide strip

    Geometry
    --------
    - Arm positioned with pivot at origin, extending in +X
    - Cam lock positioned at pivot end of arm
    - PTFE strip positioned on T-slot tongue (bottom of arm)
    """
    if cq is None:
        raise ImportError("CadQuery is required for arm_assy.build()")

    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")

    # Use provided params or default
    p = params if params is not None else _default_params

    # ── Build sub-components ──────────────────────────────────────────────────

    # Build the sliding arm (geometry already oriented for the side)
    arm_solid = sliding_arm.build(params=p, side=side)

    # Build cam lock (neutral orientation)
    cam_solid = cam_lock.build(params=p)

    # Build PTFE strip
    ptfe_solid = ptfe_slide_strip.build(params=p)

    # ── Create assembly ───────────────────────────────────────────────────────

    assembly = cq.Assembly(name=f"arm_assy_{side}")

    # Add arm at origin (arm geometry is built with pivot at origin)
    assembly.add(arm_solid.val(), name="arm")

    # Position cam lock at pivot end of arm
    # Cam lock needs to be rotated 90° about Z so lever points along arm length
    # Position centered on cam slot at pivot end
    # The arm cam slot is at x=12mm from pivot, cam lock bore is eccentric
    # Cam should sit on top of arm at the pivot end
    cam_x_offset = CAM_SLOT_CENTER_X_MM  # Center of slot on arm
    cam_y_offset = 0.0  # Centered on arm width
    cam_z_offset = p.ARM_THICKNESS_MM + p.CAM_DISC_THICKNESS_MM / 2  # On top of arm

    # Note: CAM_DISC_THICKNESS_MM is from cam_lock.py constants, not params
    from cad.components.cam_lock import CAM_DISC_THICKNESS_MM

    assembly.add(
        cam_solid.val(),
        name="cam_lock",
        loc=cq.Location(
            cq.Vector(cam_x_offset, cam_y_offset, cam_z_offset),
            cq.Vector(0, 0, 1),  # Z-axis rotation
            90.0  # Rotate 90° to align lever along arm
        )
    )

    # Position PTFE strip on T-slot tongue (bottom of arm)
    ptfe_x_offset = p.PTFE_LENGTH_MM / 2 + 15  # Center along arm length (tongue starts at 15mm)
    ptfe_y_offset = 0.0  # Centered on arm width
    ptfe_z_offset = -p.PTFE_THICKNESS_MM / 2 - p.ARM_TSLOT_ENGAGEMENT_MM / 2  # In the tongue groove

    assembly.add(
        ptfe_solid.val(),
        name="ptfe_strip",
        loc=cq.Location(cq.Vector(ptfe_x_offset, ptfe_y_offset, ptfe_z_offset))
    )

    return assembly