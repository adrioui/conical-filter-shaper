"""
Full Assembly — Universal Filter Ruler
========================================
Top-level assembly: base plate + two arm assemblies + ferrous strip + magnetic markers.

Sub-assemblies:
  - arm_assy (×2, left and right)

Components:
  - base_plate (aluminum body)
  - ferrous_strip (steel magnetic track)
  - magnetic_marker (×8, color-coded preset markers)

Origin: Base plate bottom face center at (0, 0, 0), +Z up.

Usage
-----
    import cad.assemblies.full_assy as full_assy
    assembly = full_assy.build(angle_deg=60.0)  # cq.Assembly
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import math
import cad.params as _default_params
from cad.components import base_plate, ferrous_strip, magnetic_marker
from cad.assemblies import arm_assy
from cad.utils.ruler_math import (
    arm_position_at_angle,
    pivot_position,
    ANGLE_RANGE_MIN_DEG,
    ANGLE_RANGE_MAX_DEG,
)


# Default included angle for the two arms
DEFAULT_ANGLE_DEG: float = 60.0

# Marker positioning constants
MARKER_COUNT: int = 8
MARKER_COLORS: list[str] = ["red", "blue", "green", "yellow"]
MARKER_SPACING_THRESHOLD_MM: float = 20.0  # Minimum spacing between markers


def build(
    params=None,
    angle_deg: float = DEFAULT_ANGLE_DEG,
) -> "cq.Assembly":
    """
    Build the full ruler assembly.

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
        Assembly containing the named parts:
          - "base_plate": base plate solid
          - "arm_left": left arm assembly
          - "arm_right": right arm assembly
          - "ferrous_strip": magnetic track strip
          - "marker_0" through "marker_7": magnetic markers

    Geometry
    --------
    - Base plate centered at origin, bottom face at Z=0
    - Arms pivot at origin, rotated by ±half_angle from center-line
    - Ferrous strip centered along Y-axis on top of base plate
    - Markers positioned along ferrous strip with even spacing

    Raises
    ------
    ValueError
        If angle_deg is outside the operating range (40°–85°).
    """
    if cq is None:
        raise ImportError("CadQuery is required for full_assy.build()")

    # Validate angle range
    if angle_deg < ANGLE_RANGE_MIN_DEG or angle_deg > ANGLE_RANGE_MAX_DEG:
        raise ValueError(
            f"angle_deg must be between {ANGLE_RANGE_MIN_DEG} and {ANGLE_RANGE_MAX_DEG}, "
            f"got {angle_deg}"
        )

    # Use provided params or default
    p = params if params is not None else _default_params

    # ── Build base plate ───────────────────────────────────────────────────────
    base_solid = base_plate.build(params=p)

    # ── Build arm assemblies ────────────────────────────────────────────────────
    arm_left_solid = arm_assy.build(params=p, side="left")
    arm_right_solid = arm_assy.build(params=p, side="right")

    # ── Build ferrous strip ─────────────────────────────────────────────────────
    ferrous_solid = ferrous_strip.build(params=p)

    # ── Build magnetic markers ─────────────────────────────────────────────────
    marker_solids = []
    for i, color in enumerate(MARKER_COLORS * 2):  # 2 of each color
        marker_solids.append(magnetic_marker.build(params=p, color=color))

    # ── Create assembly ────────────────────────────────────────────────────────

    assembly = cq.Assembly(name="full_ruler_assy")

    # Add base plate at origin (bottom face centered at origin)
    assembly.add(base_solid.val(), name="base_plate")

    # Get arm positioning from ruler_math
    left_transform = arm_position_at_angle(angle_deg, side="left")
    right_transform = arm_position_at_angle(angle_deg, side="right")

    # Position left arm assembly
    # The arm_assy has its origin at pivot, extends in +X
    # Rotate about Z-axis by half_angle (positive = CCW for left arm)
    left_rotation = left_transform["rotation_deg"]
    assembly.add(
        arm_left_solid.val(),
        name="arm_left",
        loc=cq.Location(
            cq.Vector(0, 0, p.BASE_THICKNESS_MM),  # Pivot at top of base plate
            cq.Vector(0, 0, 1),  # Rotate about Z
            left_rotation
        )
    )

    # Position right arm assembly
    right_rotation = right_transform["rotation_deg"]
    assembly.add(
        arm_right_solid.val(),
        name="arm_right",
        loc=cq.Location(
            cq.Vector(0, 0, p.BASE_THICKNESS_MM),  # Pivot at top of base plate
            cq.Vector(0, 0, 1),  # Rotate about Z
            right_rotation
        )
    )

    # Position ferrous strip on top of base plate, centered along Y-axis
    # The ferrous strip sits in the magnetic track recess
    ferrous_x_offset = 0.0  # Centered
    ferrous_y_offset = 0.0  # Centered
    ferrous_z_offset = p.BASE_THICKNESS_MM - p.MARKER_TRACK_RECESS_DEPTH_MM / 2

    assembly.add(
        ferrous_solid.val(),
        name="ferrous_strip",
        loc=cq.Location(cq.Vector(ferrous_x_offset, ferrous_y_offset, ferrous_z_offset))
    )

    # Position magnetic markers along the ferrous strip
    # 8 markers, evenly spaced along the 180mm track length
    # Leave some margin at ends for clearance
    track_length = p.MARKER_TRACK_LENGTH_MM
    marker_margin = 15.0  # mm from each end
    marker_spacing = (track_length - 2 * marker_margin) / (MARKER_COUNT - 1)

    for i, (marker_solid, color) in enumerate(zip(marker_solids, MARKER_COLORS * 2)):
        # Position along track (X-axis)
        marker_x = -track_length / 2 + marker_margin + i * marker_spacing
        marker_y = 0.0  # Centered on track
        marker_z = (
            p.BASE_THICKNESS_MM
            - p.MARKER_TRACK_RECESS_DEPTH_MM
            + p.MARKER_HEIGHT_MM / 2
        )  # Sitting on top of ferrous strip

        assembly.add(
            marker_solid.val(),
            name=f"marker_{i}",
            loc=cq.Location(cq.Vector(marker_x, marker_y, marker_z))
        )

    return assembly