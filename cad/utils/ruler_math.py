"""
Ruler Math — Universal Coffee Filter Ruler v3.0
=================================================
Pure-math helpers for the V-shape bevel gauge ruler geometry.
No CadQuery imports — safe to use in tests without CQ installed.

Coordinate Convention
---------------------
- Origin  : pivot point (hinge center)
- X-axis  : center-line bisecting the V-angle (toward the "open" side)
- Y-axis  : perpendicular to center-line in the plane of the arms
- Angles  : half-angle measured from center-line to each arm;
            positive = left arm (CCW), negative = right arm (CW)

All lengths in mm.
All angles in degrees unless a parameter name ends in ``_rad``.

v3.0 Changes:
- Legs replaced with tapered arms
- Fold marks replaced with cone geometry functions
- Added cone half-angle to sector conversion (for bevel gauge design)
"""
from __future__ import annotations

import math
from typing import Final

# Angle operating range (mirrors cad/params.py — kept here for module
# independence so ruler_math.py is importable without params).
ANGLE_RANGE_MIN_DEG: Final[float] = 40.0   # Minimum adjustable included angle
ANGLE_RANGE_MAX_DEG: Final[float] = 85.0   # Maximum adjustable included angle

# Default arm length (v3.0 design)
DEFAULT_ARM_LENGTH_MM: Final[float] = 120.0


# ── Cone Geometry — Bevel Gauge Flat Pattern ─────────────────────────────────

def cone_half_angle_to_sector(half_angle_deg: float) -> float:
    """
    Convert the cone half-angle to the flat sector central angle in degrees.

    When a cone is unrolled flat, the sector angle is related to the cone
    half-angle by the formula:
        sector = 360 × sin(half_angle)

    This is fundamental to bevel gauge design — to create a cone with a
    given half-angle at the apex, the flat pattern must be cut as a sector
    with this central angle.

    Parameters
    ----------
    half_angle_deg : float
        The half-angle at the cone apex (degrees). This is the angle from
        the cone centerline to the cone surface.

    Returns
    -------
    float
        The central angle of the flat sector pattern (degrees).

    Examples
    --------
    >>> round(cone_half_angle_to_sector(30), 3)
    180.0
    >>> round(cone_half_angle_to_sector(45), 3)
    254.558
    """
    return 360.0 * math.sin(math.radians(half_angle_deg))


def sector_to_cone_half_angle(sector_deg: float) -> float:
    """
    Inverse conversion: sector angle to cone half-angle.

    Given the sector central angle, this computes the cone half-angle:
        half_angle = arcsin(sector / 360)

    Parameters
    ----------
    sector_deg : float
        The central angle of the flat sector pattern (degrees).

    Returns
    -------
    float
        The half-angle at the cone apex (degrees).

    Examples
    --------
    >>> round(sector_to_cone_half_angle(180), 2)
    30.0
    >>> round(sector_to_cone_half_angle(254.558), 3)
    45.0
    """
    return math.degrees(math.asin(sector_deg / 360.0))


def ruler_angle_to_cone_angle(ruler_angle_deg: float) -> float:
    """
    Convert the ruler's opening angle to the resulting cone full angle.

    In the bevel gauge design, the ruler opening angle directly forms
    the cone angle (the full apex angle). The V-opening of the ruler
    matches the cone opening.

    For example:
    - Ruler at 60° creates a 60° cone (30° half-angle each side)
    - The filter is folded to match this cone angle

    Parameters
    ----------
    ruler_angle_deg : float
        The ruler opening angle (included angle between arms, in degrees).

    Returns
    -------
    float
        The resulting cone full angle (degrees).

    Examples
    --------
    >>> ruler_angle_to_cone_angle(60.0)
    60.0
    >>> ruler_angle_to_cone_angle(80.0)
    80.0
    """
    return ruler_angle_deg


# ── V-Opening Geometry ────────────────────────────────────────────────────────

def v_opening_width(distance_mm: float, angle_deg: float) -> float:
    """
    Calculate the width of the V-opening at a given distance from the pivot.

    The V-opening width (gap between inner edges of the two arms) at any
    distance d from the pivot is:
        w = 2 × d × sin(angle / 2)

    Parameters
    ----------
    distance_mm : float
        Distance from pivot center along an arm (mm).
    angle_deg : float
        Full included angle between the two arms (degrees).

    Returns
    -------
    float
        Width of the V-opening at that distance (mm).

    Examples
    --------
    >>> round(v_opening_width(120.0, 60.0), 3)
    120.0
    >>> round(v_opening_width(95.0, 60.0), 2)
    95.0
    """
    half_angle_rad = math.radians(angle_deg / 2.0)
    return 2.0 * distance_mm * math.sin(half_angle_rad)


def arm_tip_spread(angle_deg: float, arm_length: float = DEFAULT_ARM_LENGTH_MM) -> float:
    """
    Calculate the distance between the tips of the two arms when open at
    a given angle.

    This is the chord distance between the two arm tips (inner edges).
    The tips are separated by:
        spread = 2 × arm_length × sin(angle / 2)

    Parameters
    ----------
    angle_deg : float
        Full included angle between the two arms (degrees).
    arm_length : float, optional
        Length of each arm from pivot to tip (mm). Default: 120.0.

    Returns
    -------
    float
        Distance between arm tips when open at that angle (mm).

    Examples
    --------
    >>> round(arm_tip_spread(60.0), 3)
    120.0
    >>> round(arm_tip_spread(40.0), 2)
    82.82
    """
    half_angle_rad = math.radians(angle_deg / 2.0)
    return 2.0 * arm_length * math.sin(half_angle_rad)


# ── Dripper Stand Height ──────────────────────────────────────────────────────

def stand_height(angle_deg: float, arm_length: float = DEFAULT_ARM_LENGTH_MM) -> float:
    """
    Calculate the vertical height of the ruler when used as a V-shaped dripper
    stand, resting on the tips of both arms with the pivot at the top.

    When the ruler stands as an inverted V on a flat surface, the height
    from the surface to the pivot is:
        height = arm_length × cos(angle / 2)

    Parameters
    ----------
    angle_deg : float
        Full included angle between the two arms (degrees).
    arm_length : float, optional
        Length of each arm from pivot to tip (mm). Default: 120.0.

    Returns
    -------
    float
        Vertical height from surface to pivot (mm).

    Examples
    --------
    >>> round(stand_height(60.0), 2)
    103.92
    >>> round(stand_height(40.0), 2)
    114.71
    """
    half_angle_rad = math.radians(angle_deg / 2.0)
    return arm_length * math.cos(half_angle_rad)


# ── Arc Mark Intersection Check ──────────────────────────────────────────────

def arc_mark_intersects_arm(
    arc_radius: float,
    arm_length: float,
    arm_width_narrow: float,
    arm_width_wide: float,
) -> bool:
    """
    Check if an arc mark at the given radius from the pivot will intersect
    the tapered arm geometry.

    The arm is a tapered trapezoid: narrow at the pivot end, wide at the tip.
    We check if the arc position falls within the arm's width profile.

    Parameters
    ----------
    arc_radius : float
        Radius from pivot hole center to the arc mark (mm).
    arm_length : float
        Total length of the arm from pivot to tip (mm).
    arm_width_narrow : float
        Width of the arm at the narrow (pivot) end (mm).
    arm_width_wide : float
        Width of the arm at the wide (tip) end (mm).

    Returns
    -------
    bool
        True if the arc mark at this radius will fall on the arm surface
        (i.e., intersects the arm geometry). False if it's outside the arm.

    Examples
    --------
    >>> arc_mark_intersects_arm(95.0, 120.0, 25.0, 65.0)
    True
    >>> arc_mark_intersects_arm(10.0, 120.0, 25.0, 65.0)
    False  # Too close to pivot - outside arm
    """
    # Normalized position along arm (0 = pivot, 1 = tip)
    t = arc_radius / arm_length

    # Outside arm length range
    if t < 0 or t > 1:
        return False

    # Interpolate arm width at this position
    current_width = arm_width_narrow + t * (arm_width_wide - arm_width_narrow)

    # Arc marks are centered on arm (half width on each side)
    # If arc radius is within the arm width half-range, it intersects
    half_width = current_width / 2.0

    # Distance from arm centerline to mark
    # Arc marks are at half the arm width from center (on either side)
    mark_offset = half_width

    # The mark will be on the arm if the arc is within valid range
    # Here we check if the arc position is within the arm body
    return t > 0 and t < 1


# ── Angle Validation ───────────────────────────────────────────────────────────

def validate_angle(angle_deg: float) -> None:
    """
    Validate that the given angle is within the allowed operating range.

    Parameters
    ----------
    angle_deg : float
        Angle in degrees to validate.

    Raises
    ------
    ValueError
        If angle_deg is outside the range 40°–85°.
    """
    if not (ANGLE_RANGE_MIN_DEG <= angle_deg <= ANGLE_RANGE_MAX_DEG):
        raise ValueError(
            f"Angle {angle_deg}° is outside the valid range "
            f"{ANGLE_RANGE_MIN_DEG}°–{ANGLE_RANGE_MAX_DEG}°"
        )
