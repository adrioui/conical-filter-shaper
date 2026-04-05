"""
Base Cap / Ring Retainer — 6061-T6 Aluminium, CNC turned + anodized.

Snap-locks onto the bottom of the Handle Housing. Retains the Angle-Set Ring
axially (prevents ring extraction). User-accessible to disassemble for cleaning.

Origin: outer face (bottom, user-visible) at (0,0,0), +Z toward housing.
Material: 6061-T6 Al — same finish family as Handle Housing
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Workplane
    """
    Build the Base Cap.

    V1 honesty notes:
        - The snap-retention detail is simplified to a recessed top face that leaves an outer lip.
        - Flexural undercut and exact assembly retention behavior are deferred.
    """
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    cap = (
        cq.Workplane("XY")
        .circle(params.BASE_CAP_OD_MM / 2.0)
        .circle(params.CAM_RING_BORE_MM / 2.0)
        .extrude(params.BASE_CAP_THICKNESS_MM)
    )

    rebate_radius = max(
        (params.BASE_CAP_OD_MM / 2.0) - params.BASE_CAP_SNAP_LIP_MM,
        (params.CAM_RING_BORE_MM / 2.0) + 1.0,
    )
    rebate = (
        cq.Workplane("XY", origin=(0.0, 0.0, params.BASE_CAP_THICKNESS_MM - params.BASE_CAP_SNAP_DEPTH_MM))
        .circle(rebate_radius)
        .extrude(params.BASE_CAP_SNAP_DEPTH_MM)
    )
    return cap.cut(rebate)
