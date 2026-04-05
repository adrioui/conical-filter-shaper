"""
Ejection Push Rod — SS 304, CNC turned, h6 ground finish.

Slides inside the Tip Insert Block axial bore (H7/h6 fit).
At rest: rod tip recessed EJECTION_ROD_RECESS_MM below tip dimple face.
On press: extends EJECTION_STROKE_MM to break filter adhesion.

Origin: rod tip (bottom, filter contact end) at (0,0,0), +Z toward button.
Material: params.EJECTION_ROD_MATERIAL
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Workplane
    """
    Build the Ejection Push Rod.

    V1 honesty notes:
        - The top-end snap-fit groove for the button cap is not parameterized yet.
        - The convex tip is approximated by a small edge fillet rather than an exact R10 cap.
    """
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    rod = (
        cq.Workplane("XY")
        .circle(params.EJECTION_ROD_DIAMETER_MM / 2.0)
        .extrude(params.EJECTION_ROD_LENGTH_MM)
    )
    return rod.faces("<Z").edges().fillet(0.1)
