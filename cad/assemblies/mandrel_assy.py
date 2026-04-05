"""
Mandrel Sub-Assembly: Shell L + Shell R + Tip Insert Block + Hinge Pin + Seam Guide Fin.

Both shells are positioned at the given preset's spread angle.
Shells are hinged at the tip insert block (apex).
Fin inserted at default guide position (params.FIN_DEFAULT_GUIDE_POSITION_MM).
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params
from cad.components import overlap_fin, shell_half_l, shell_half_r, tip_insert_block


def build(params=None, preset=None):  # -> cq.Assembly
    if params is None:
        params = _default_params
    if preset is None:
        preset = params.DEFAULT_PRESET

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    shell_l = shell_half_l.build(params=params, preset=preset)
    shell_r = shell_half_r.build(params=params, preset=preset)
    tip_block = tip_insert_block.build(params=params)
    fin = overlap_fin.build(params=params)
    hinge_pin = cq.Workplane("YZ").circle(params.TIP_HINGE_BORE_DIA_MM / 2.0).extrude(params.TIP_BLOCK_WIDTH_MM)

    assy = cq.Assembly(name="mandrel_assy")
    assy.add(shell_l, name="shell_half_l")
    assy.add(shell_r, name="shell_half_r")
    assy.add(tip_block, name="tip_insert_block")
    assy.add(
        hinge_pin,
        name="hinge_pin",
        loc=cq.Location(cq.Vector(-params.TIP_BLOCK_WIDTH_MM / 2.0, 0.0, params.TIP_HINGE_BORE_Z_MM)),
    )
    assy.add(
        fin,
        name="seam_guide_fin",
        loc=cq.Location(cq.Vector(params.FIN_WIDTH_MM / 2.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0), 90.0),
    )
    return assy
