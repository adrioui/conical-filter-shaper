"""
Handle Housing — 6061-T6 Aluminium, CNC turned + milled + Type II anodized.

Structural chassis. Contains:
  - Cam ring bore (captures ring + PTFE washers)
  - Detent blind pocket (tangential to ring bore)
  - Angle indicator window slot
  - Ejection rod guide bore (axial, top face)
  - Grip zone (knurled or accepts grip insert)

Origin: top face center at (0, 0, 0), +Z up.
Material: params.HOUSING_MATERIAL
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Workplane
    """
    Build the Handle Housing.

    V1 honesty notes:
        - The grip knurl is a process/drawing callout and is not modelled.
        - Assembly screw holes are still not parameterized and are omitted.
        - Detent pocket and angle window are nominal visualization features, not tolerance-verified details.
    """
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    flange_r = params.HOUSING_FLANGE_OD_MM / 2.0
    handle_r = params.HANDLE_OD_MM / 2.0
    flange_h = params.HOUSING_FLANGE_HEIGHT_MM
    transition_h = params.HOUSING_TRANSITION_CHAMFER_MM
    total_h = params.HOUSING_FLANGE_HEIGHT_MM + params.HANDLE_LENGTH_MM

    outer = (
        cq.Workplane("XZ")
        .polyline([
            (0.0, 0.0),
            (flange_r, 0.0),
            (flange_r, -(flange_h - transition_h)),
            (handle_r, -flange_h),
            (handle_r, -total_h),
            (0.0, -total_h),
        ])
        .close()
        .revolve(360, (0, 0, 0), (0, 1, 0))
    )

    ring_bore_depth = flange_h - params.HOUSING_RING_BORE_FLOOR_MM
    housing = outer.faces(">Z").workplane().hole(params.HOUSING_RING_BORE_MM, ring_bore_depth)
    housing = housing.faces(">Z").workplane().hole(params.EJECTION_GUIDE_BORE_DIA_MM, total_h)

    detent_x = (params.HOUSING_RING_BORE_MM / 2.0) + (params.DETENT_POCKET_DIA_MM / 2.0)
    detent = cq.Solid.makeCylinder(
        params.DETENT_POCKET_DIA_MM / 2.0,
        params.DETENT_POCKET_DEPTH_MM,
        pnt=cq.Vector(detent_x, flange_r + 1.0, -(flange_h / 2.0)),
        dir=cq.Vector(0.0, -1.0, 0.0),
    )
    housing = housing.cut(cq.Workplane("XY").add(detent))

    window = (
        cq.Workplane("XY")
        .box(
            params.ANGLE_WINDOW_WIDTH_MM,
            params.HOUSING_FLANGE_OD_MM,
            params.ANGLE_WINDOW_HEIGHT_MM,
            centered=(True, True, True),
        )
        .translate((0.0, 0.0, -(flange_h / 2.0)))
        .rotate((0, 0, 0), (0, 0, 1), 45.0)
    )
    return housing.cut(window)
