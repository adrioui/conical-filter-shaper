"""
Ejection Sub-Assembly: Ejection Rod + Return Spring + Button Cap.
Rod is in the rest (retracted) position by default.
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params
from cad.components import ejection_rod


def build(params=None):  # -> cq.Assembly
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    rod = ejection_rod.build(params=params)
    spring = (
        cq.Workplane("XY")
        .circle(params.TIP_EJECTION_BORE_DIA_MM / 2.0)
        .circle(params.EJECTION_ROD_DIAMETER_MM / 2.0)
        .extrude(params.EJECTION_SPRING_FREE_LENGTH_MM)
    )
    button_thickness = params.EJECTION_BUTTON_DIAMETER_MM / 2.0
    button = (
        cq.Workplane("XY")
        .circle(params.EJECTION_BUTTON_DIAMETER_MM / 2.0)
        .extrude(button_thickness)
    )

    assy = cq.Assembly(name="ejection_assy")
    assy.add(rod, name="rod")
    assy.add(
        spring,
        name="spring",
        loc=cq.Location(cq.Vector(0.0, 0.0, params.EJECTION_ROD_LENGTH_MM - params.EJECTION_SPRING_FREE_LENGTH_MM)),
    )
    assy.add(
        button,
        name="button_cap",
        loc=cq.Location(cq.Vector(0.0, 0.0, params.EJECTION_ROD_LENGTH_MM)),
    )
    return assy
