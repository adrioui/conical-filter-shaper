"""
Handle Grip Insert — NBR-70 overmold or TPU sleeve.

Provides a slip-resistant food-safe grip surface over the Handle Housing grip zone.
Modelled as a hollow cylinder (reference geometry for overmold tooling or sleeve cut).

Origin: top face center at (0,0,0), +Z up (matches handle_housing.py origin).
Material: NBR-70 (food-grade, FDA 21 CFR 177.2600) or Shore-A 70 TPU
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Workplane
    """
    Build the grip insert reference geometry.

    V1 honesty notes:
        - This is reference sleeve geometry only.
        - Surface texture, rubber compliance, and bonding details are not modelled.
    """
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    outer_radius = (params.HANDLE_OD_MM + 2.0 * params.GRIP_INSERT_WALL_MM) / 2.0
    inner_radius = params.HANDLE_OD_MM / 2.0
    return (
        cq.Workplane("XY")
        .circle(outer_radius)
        .circle(inner_radius)
        .extrude(-params.HANDLE_LENGTH_MM)
    )
