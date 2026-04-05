"""
Tip Insert Block — SS 316L apex anchor.

Functions:
  1. Structural apex anchor (hinge pin bore, transverse)
  2. Tip locator dimple for the closed paper apex
  3. Ejection rod chamber at the tool axis

Origin: dimple-face center point at (0, 0, 0). +Z toward ejection button.
Block: params.TIP_BLOCK_WIDTH_MM × params.TIP_BLOCK_DEPTH_MM × params.TIP_BLOCK_HEIGHT_MM
Material: params.TIP_MATERIAL
"""
from __future__ import annotations

import math

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Workplane
    """
    Build the Tip Insert Block.

    Modelled geometry:
        - SS316L block body with external edge fillets
        - conical tip dimple on the dimple face (Z=0 datum)
        - hinge bore along the X axis
        - blind 4.0 mm axial ejection chamber from the +Z face
        - 3.0 mm axial guide bore linking the chamber to the dimple region

    Honest limitation:
        This is still a nominal V1 ejection-stack model, not a fully validated production
        detail. The cross-drilled hinge/guide region and exact rod-tip / paper-contact
        behavior still need physical validation.
    """
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    width = params.TIP_BLOCK_WIDTH_MM
    depth = params.TIP_BLOCK_DEPTH_MM
    height = params.TIP_BLOCK_HEIGHT_MM

    block = (
        cq.Workplane("XY")
        .box(width, depth, height, centered=(True, True, False))
        .edges("%Line")
        .fillet(params.TIP_EXTERNAL_EDGE_FILLET_MM)
    )

    # Tip dimple: conical pocket starting from the dimple-face datum (Z=0) into +Z.
    opening_radius = params.TIP_DIMPLE_DIAMETER_MM / 2.0
    dimple_depth = params.TIP_DIMPLE_DEPTH_MM
    dimple_half_angle_rad = math.radians(params.TIP_DIMPLE_INCLUDED_ANGLE_DEG / 2.0)
    tip_radius = max(0.01, opening_radius - dimple_depth * math.tan(dimple_half_angle_rad))
    dimple = cq.Solid.makeCone(
        opening_radius,
        tip_radius,
        dimple_depth,
        pnt=cq.Vector(0.0, 0.0, 0.0),
        dir=cq.Vector(0.0, 0.0, 1.0),
    )
    block = block.cut(cq.Workplane("XY").add(dimple))

    # Break the dimple mouth edge to reduce paper snag / tear risk.
    block = block.faces("<Z").edges("%Circle").fillet(params.TIP_DIMPLE_EDGE_FILLET_MM)

    # Main ejection chamber: intentionally blind from +Z so the dimple surface is preserved.
    chamber_depth = params.TIP_EJECTION_CHAMBER_DEPTH_MM
    chamber = cq.Solid.makeCylinder(
        params.TIP_EJECTION_BORE_DIA_MM / 2.0,
        chamber_depth,
        pnt=cq.Vector(0.0, 0.0, height - chamber_depth),
        dir=cq.Vector(0.0, 0.0, 1.0),
    )
    block = block.cut(cq.Workplane("XY").add(chamber))

    # Guide bore: nominal 3.0 mm rod path between the chamber floor and the dimple region.
    guide_bore_bottom_z = params.EJECTION_ROD_RECESS_MM
    guide_bore_top_z = height - chamber_depth
    guide_bore_length = guide_bore_top_z - guide_bore_bottom_z
    if guide_bore_length > 0:
        guide_bore = cq.Solid.makeCylinder(
            params.EJECTION_GUIDE_BORE_DIA_MM / 2.0,
            guide_bore_length,
            pnt=cq.Vector(0.0, 0.0, guide_bore_bottom_z),
            dir=cq.Vector(0.0, 0.0, 1.0),
        )
        block = block.cut(cq.Workplane("XY").add(guide_bore))

    # Hinge bore: transverse, aligned to the X axis at the parameterized Z datum.
    hinge_cutter = cq.Solid.makeCylinder(
        params.TIP_HINGE_BORE_DIA_MM / 2.0,
        width + 2.0,
        pnt=cq.Vector(-(width / 2.0) - 1.0, 0.0, params.TIP_HINGE_BORE_Z_MM),
        dir=cq.Vector(1.0, 0.0, 0.0),
    )
    block = block.cut(cq.Workplane("XY").add(hinge_cutter))

    return block
