"""
Ring Sub-Assembly: Cam Ring + 2× PTFE Bearing Washers + Handle Housing.
Ring is positioned at the preset's dwell angle (click position).
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params
from cad.components import cam_ring, handle_housing


def build(params=None, preset=None):  # -> cq.Assembly
    if params is None:
        params = _default_params
    if preset is None:
        preset = params.DEFAULT_PRESET

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    housing = handle_housing.build(params=params)
    ring = cam_ring.build(params=params)
    washer = (
        cq.Workplane("XY")
        .circle(params.CAM_RING_OD_MM / 2.0)
        .circle(params.CAM_RING_BORE_MM / 2.0)
        .extrude(-params.PTFE_WASHER_THICKNESS_MM)
    )

    preset_index = params.PRESETS.index(preset)
    ring_angle = preset_index * params.CAM_RING_CLICK_DEG
    ring_center_z = -(params.PTFE_WASHER_THICKNESS_MM + (params.CAM_RING_THICKNESS_MM / 2.0))
    bottom_washer_z = -(params.PTFE_WASHER_THICKNESS_MM + params.CAM_RING_THICKNESS_MM)

    assy = cq.Assembly(name="ring_assy")
    assy.add(housing, name="handle_housing")
    assy.add(washer, name="washer_top")
    assy.add(
        ring,
        name="cam_ring",
        loc=cq.Location(cq.Vector(0.0, 0.0, ring_center_z), cq.Vector(0.0, 0.0, 1.0), ring_angle),
    )
    assy.add(
        washer,
        name="washer_bottom",
        loc=cq.Location(cq.Vector(0.0, 0.0, bottom_washer_z)),
    )
    return assy
