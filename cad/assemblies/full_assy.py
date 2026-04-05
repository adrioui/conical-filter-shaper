"""
Full Assembly — all sub-assemblies combined.

Sub-assemblies composed:
  - mandrel_assy  (shells + tip insert + fin)
  - ring_assy     (cam ring + PTFE washers inside handle housing)
  - ejection_assy (rod + spring + button cap)

Origin: handle housing top face center at (0,0,0), +Z up (apex up orientation).
Preset: caller specifies which ConePreset to use for shell spread geometry.
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params
from cad.assemblies import mandrel_assy, ring_assy, ejection_assy
from cad.components import base_cap, handle_grip_insert


def build(params=None, preset=None):  # -> cq.Assembly
    """
    Build the full tool assembly.

    V1 honesty notes:
        - Assembly placement is nominal and intended for visualization/export.
        - No tolerance stack-up, interference resolution, or motion simulation is performed.
    """
    if params is None:
        params = _default_params
    if preset is None:
        preset = params.DEFAULT_PRESET

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    ring = ring_assy.build(params=params, preset=preset)
    mandrel = mandrel_assy.build(params=params, preset=preset)
    ejection = ejection_assy.build(params=params)
    cap = base_cap.build(params=params)
    grip = handle_grip_insert.build(params=params)

    housing_bottom_z = -(params.HOUSING_FLANGE_HEIGHT_MM + params.HANDLE_LENGTH_MM)
    base_cap_outer_face_z = housing_bottom_z - params.BASE_CAP_THICKNESS_MM

    assy = cq.Assembly(name="full_assy")
    assy.add(ring, name="ring")
    assy.add(mandrel, name="mandrel")
    assy.add(
        ejection,
        name="ejection",
        loc=cq.Location(cq.Vector(0.0, 0.0, params.EJECTION_ROD_RECESS_MM)),
    )
    assy.add(
        grip,
        name="grip_insert",
        loc=cq.Location(cq.Vector(0.0, 0.0, 0.0)),
    )
    assy.add(
        cap,
        name="base_cap",
        loc=cq.Location(cq.Vector(0.0, 0.0, base_cap_outer_face_z)),
    )
    return assy
