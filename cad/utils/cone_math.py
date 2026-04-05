"""
Cone geometry helpers.
Pure math — no CadQuery imports. Safe for use in tests and scripts without a CQ install.
All angles in degrees. All lengths in mm.
"""
from __future__ import annotations
import math


def base_radius(slant_height_mm: float, half_angle_deg: float) -> float:
    """r = L × sin(α_half)"""
    return slant_height_mm * math.sin(math.radians(half_angle_deg))


def axial_height(slant_height_mm: float, half_angle_deg: float) -> float:
    """h = L × cos(α_half)"""
    return slant_height_mm * math.cos(math.radians(half_angle_deg))


def slant_height(base_radius_mm: float, half_angle_deg: float) -> float:
    """L = r / sin(α_half)"""
    return base_radius_mm / math.sin(math.radians(half_angle_deg))


def included_angle_from_radii(base_radius_mm: float, slant_height_mm: float) -> float:
    """Back-calculate full included angle from measured base radius and slant height."""
    half = math.degrees(math.asin(base_radius_mm / slant_height_mm))
    return 2.0 * half


def half_angle(included_angle_deg: float) -> float:
    """Return the half-angle from a full included angle."""
    return included_angle_deg / 2.0


def cone_solid_angle_sr(half_angle_deg: float) -> float:
    """Solid angle of a cone in steradians (useful for filter coverage checks)."""
    return 2.0 * math.pi * (1.0 - math.cos(math.radians(half_angle_deg)))


def equivalent_flat_blank_radius_for_slant(slant_mm: float) -> float:
    """
    Return the radius of an equivalent flat paper blank for this slant height.

    This is a geometry helper only. V1 workflow uses pre-seamed conical papers rather
    than flat circular blanks, but the equivalence is still useful for back-calculation.
    For a full disc (360°): blank_radius = slant_height.
    """
    return slant_mm


def filter_disc_radius_for_slant(slant_mm: float) -> float:
    """Deprecated alias for equivalent_flat_blank_radius_for_slant()."""
    return equivalent_flat_blank_radius_for_slant(slant_mm)
