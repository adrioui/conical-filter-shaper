"""
Ruler Math — Universal Filter Ruler
=====================================
Pure-math helpers for the flat-ruler angle and geometry calculations.
No CadQuery imports — safe to use in tests without CQ installed.

Coordinate Convention
---------------------
- Origin  : pivot point of arms (center-top of base plate)
- X-axis  : along base plate length (200 mm direction; ← left, → right)
- Y-axis  : along base plate width  (120 mm direction; ↓ toward bottom edge)
- Angles  : half-angle measured from center-line to arm inner edge;
            positive half-angle = left arm; negative = right arm

All lengths in mm.
All angles in degrees unless a parameter name ends in ``_rad``.
"""
from __future__ import annotations

import math
from typing import TypedDict

# Angle operating range (mirrors cad/params.py constants — kept here for
# module independence so ruler_math.py is importable without params).
ANGLE_RANGE_MIN_DEG: float = 40.0   # Minimum adjustable included angle
ANGLE_RANGE_MAX_DEG: float = 85.0   # Maximum adjustable included angle


# ── Arm spread ────────────────────────────────────────────────────────────────

def angle_to_arm_spread(angle_deg: float, arm_length: float) -> float:
    """
    Compute the lateral (tip-to-tip) spread distance between the two arm tips
    at the given included angle.

    The formula follows directly from symmetry:
        spread = 2 × arm_length × sin(half_angle)

    Parameters
    ----------
    angle_deg : float
        Full included angle between the two arm inner edges (degrees).
        Valid range: 40°–85°.
    arm_length : float
        Length of each sliding arm from pivot to tip (mm).

    Returns
    -------
    float
        Perpendicular (lateral) distance between the two arm tips (mm).

    Examples
    --------
    >>> round(angle_to_arm_spread(60.0, 150.0), 3)
    150.0
    >>> round(angle_to_arm_spread(40.0, 150.0), 2)
    102.61
    """
    half_angle_rad = math.radians(angle_deg / 2.0)
    return 2.0 * arm_length * math.sin(half_angle_rad)


# ── Pivot position ────────────────────────────────────────────────────────────

def pivot_position() -> tuple[float, float]:
    """
    Return the (x, y) position of the arm pivot in base-plate coordinates.

    The coordinate origin *is* the pivot, so this always returns (0, 0).
    It exists as an explicit function to make the intent clear in higher-level
    assembly code and to provide a single place to change if the pivot is ever
    offset from the geometric center.

    Returns
    -------
    tuple[float, float]
        (x, y) = (0.0, 0.0) — pivot is the coordinate origin.
    """
    return (0.0, 0.0)


# ── Arm transform ─────────────────────────────────────────────────────────────

class ArmTransform(TypedDict):
    """Transform data for one sliding arm."""
    pivot_x: float       # X coordinate of pivot (mm)
    pivot_y: float       # Y coordinate of pivot (mm)
    rotation_deg: float  # Rotation from center-line (positive = left / CCW)
    side: str            # "left" or "right"


def arm_position_at_angle(
    angle_deg: float,
    side: str = "left",
) -> ArmTransform:
    """
    Return the geometric transform for one sliding arm at the given included angle.

    Both arms share the same pivot; they differ only in rotation direction:
      - left  arm: rotated +half_angle (counter-clockwise from center-line)
      - right arm: rotated −half_angle (clockwise from center-line)

    Parameters
    ----------
    angle_deg : float
        Full included angle between the two arm inner edges (degrees).
    side : str
        Which arm: ``"left"`` or ``"right"``.

    Returns
    -------
    ArmTransform
        Dictionary with ``pivot_x``, ``pivot_y``, ``rotation_deg``, and ``side``.

    Raises
    ------
    ValueError
        If *side* is not ``"left"`` or ``"right"``.

    Examples
    --------
    >>> t = arm_position_at_angle(60.0, "left")
    >>> t["rotation_deg"]
    30.0
    >>> t = arm_position_at_angle(60.0, "right")
    >>> t["rotation_deg"]
    -30.0
    """
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")

    half_angle = angle_deg / 2.0
    px, py = pivot_position()

    return ArmTransform(
        pivot_x=px,
        pivot_y=py,
        rotation_deg=+half_angle if side == "left" else -half_angle,
        side=side,
    )


# ── Overlap calculation ───────────────────────────────────────────────────────

def overlap_for_filter(filter_radius: float, angle_deg: float) -> float:
    """
    Estimate the seam overlap (mm) when a circular filter paper of the given
    radius is folded along the two arm edges at the given included angle.

    Model (sagitta / versine):
        overlap = filter_radius × (1 − cos(half_angle))

    This represents the depth of the arc segment between the two fold lines at
    the outer edge of the filter paper — i.e. how far each half of the paper
    extends past the other when the cone is formed.

    The formula yields values in the 0–20 mm range for the supported filter
    sizes (R55–R92.5 mm) and angle range (40°–85°).

    Parameters
    ----------
    filter_radius : float
        Radius of the filter paper circle (mm).
        Typical values: 55.0 (01), 77.5 (02), 92.5 (03).
    angle_deg : float
        Full included angle between arm inner edges (degrees, 40°–85°).

    Returns
    -------
    float
        Seam overlap in mm.

    Examples
    --------
    >>> round(overlap_for_filter(77.5, 60.0), 2)
    10.38
    """
    half_angle_rad = math.radians(angle_deg / 2.0)
    return filter_radius * (1.0 - math.cos(half_angle_rad))


# ── Vernier scale ─────────────────────────────────────────────────────────────

def vernier_scale_position(
    angle_deg: float,
    vernier_radius_mm: float = 100.0,
    resolution_deg: float = 0.5,
) -> float:
    """
    Compute the arc-length position on the vernier scale for the given angle,
    measured from the minimum-angle reference (40°).

    The vernier scale is an arc engraved on the sliding arm at ``vernier_radius_mm``
    from the pivot.  Its resolution is ``resolution_deg`` per graduation (0.5° by
    default, matching the spec).

    Position formula:
        position = vernier_radius × (angle − min_angle) × π / 180

    Parameters
    ----------
    angle_deg : float
        Current included angle (degrees, 40°–85°).
    vernier_radius_mm : float
        Radial distance from pivot to the vernier scale arc (mm).
        Default: 100 mm (approximately ⅔ of arm length).
    resolution_deg : float
        Angular resolution of one vernier graduation (degrees).
        Default: 0.5°.

    Returns
    -------
    float
        Arc-length from the 40° reference mark to the current angle mark (mm).

    Examples
    --------
    >>> vernier_scale_position(40.0)
    0.0
    >>> round(vernier_scale_position(85.0), 2)
    78.54
    """
    angle_from_min = angle_deg - ANGLE_RANGE_MIN_DEG
    return vernier_radius_mm * math.radians(angle_from_min)


# ── Legacy helpers (kept for backward compatibility) ──────────────────────────

def arm_tip_x(arm_length_mm: float, half_angle_deg: float) -> float:
    """
    X-coordinate of the arm tip (along the arm center-line from pivot).

    Parameters
    ----------
    arm_length_mm : float
        Length of the sliding arm (mm).
    half_angle_deg : float
        Half the included angle (degrees from center-line).

    Returns
    -------
    float
        X distance of arm tip from pivot (mm).
    """
    return arm_length_mm * math.cos(math.radians(half_angle_deg))


def arm_tip_y(arm_length_mm: float, half_angle_deg: float) -> float:
    """
    Y-coordinate of the arm tip (lateral offset from center-line).

    Parameters
    ----------
    arm_length_mm : float
        Length of the sliding arm (mm).
    half_angle_deg : float
        Half the included angle (degrees from center-line).

    Returns
    -------
    float
        Y offset of arm tip from pivot (mm).
    """
    return arm_length_mm * math.sin(math.radians(half_angle_deg))


def included_angle_from_half(half_angle_deg: float) -> float:
    """Return full included angle from half-angle (trivial; for readability)."""
    return 2.0 * half_angle_deg


def half_angle_from_included(included_angle_deg: float) -> float:
    """Return half-angle from full included angle."""
    return included_angle_deg / 2.0


def vernier_offset_mm(
    half_angle_deg: float,
    vernier_resolution_deg: float,
    vernier_radius_mm: float,
) -> float:
    """
    Arc length corresponding to one vernier division on the arm scale.

    Parameters
    ----------
    half_angle_deg : float
        Half included angle at the measurement point (degrees).
    vernier_resolution_deg : float
        Angular resolution of vernier (e.g. 0.5°).
    vernier_radius_mm : float
        Radial distance from pivot to vernier scale (mm).

    Returns
    -------
    float
        Linear distance between adjacent vernier graduations (mm).
    """
    return vernier_radius_mm * math.radians(vernier_resolution_deg)
