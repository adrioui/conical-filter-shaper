"""
Half-Shell R — right half of the split-shell mandrel.

Identical to Shell L except:
  - Spans the +X half-plane
  - Adds radial fin slot (params.FIN_SLOT_*) on the seam-side outer face
  - ▶ Default seam-guide fin position (10 mm) marked on outer surface

Origin: cone apex at (0, 0, 0), cone axis along +Z.
Material: params.SHELL_MATERIAL
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params
from cad.components import shell_half_l


def build(params=None, preset=None):  # -> cq.Workplane
    """
    Build Half-Shell R as a CadQuery Workplane.

    Key dims vs Shell L:
        Adds: fin slot width=params.FIN_SLOT_WIDTH_MM, depth=params.FIN_SLOT_DEPTH_MM
        Slot runs axially from apex-side toward base.
        Shell R is otherwise the mirror image of Shell L about the YZ plane.
    """
    if params is None:
        params = _default_params
    if preset is None:
        preset = params.DEFAULT_PRESET

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    shell = shell_half_l.build(params=params, preset=preset).mirror(
        mirrorPlane="YZ",
        basePointVector=(0, 0, 0),
    )

    # V1 honesty note: the seam-guide slot is a nominal cut only; insertion depth and
    # protrusion tuning remain assembly-level behavior.
    slot_length = min(params.FIN_SLOT_LENGTH_MM, preset.axial_height_mm + params.SHELL_BASE_TAB_EXTENSION_MM)
    fin_slot_solid = cq.Solid.makeBox(
        params.FIN_SLOT_DEPTH_MM + 0.01,
        params.FIN_SLOT_WIDTH_MM,
        slot_length,
        pnt=cq.Vector(0.0, -params.FIN_SLOT_WIDTH_MM / 2.0, 0.0),
    )
    return shell.cut(cq.Workplane("XY").add(fin_slot_solid))
