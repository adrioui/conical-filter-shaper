"""
Shared shell-half geometry helpers.

These helpers intentionally build a simplified but coherent V1 shell:
- conical shell from true-angle cone primitives
- half split at the YZ plane
- rectangular base tab for the follower boss region
- hinge and follower bores
- optional seam-guide fin slot on Shell R

They do NOT attempt to model every manufacturing nuance yet.
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build_half_shell(params, preset, side: str = "left", include_fin_slot: bool = False):
    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    side_sign = -1.0 if side == "left" else 1.0
    outer_r = preset.base_radius_mm
    height = preset.axial_height_mm
    wall = params.SHELL_WALL_THICKNESS_MM
    tab_ext = params.SHELL_BASE_TAB_EXTENSION_MM
    follower_boss = params.SHELL_FOLLOWER_BOSS_OD_MM

    # V1 honesty notes:
    # - shell thickness is approximated by a nested cone subtraction, not a true normal-offset shell
    # - the apex region is left simplified around the hinge zone
    # - seam chamfer is applied opportunistically; if the kernel rejects it, the solid still returns

    outer_cone = cq.Solid.makeCone(0.0, outer_r, height, pnt=cq.Vector(0, 0, 0), dir=cq.Vector(0, 0, 1))
    inner_cone = cq.Solid.makeCone(
        0.0,
        max(outer_r - wall, 0.5),
        max(height - wall, 1.0),
        pnt=cq.Vector(0, 0, wall),
        dir=cq.Vector(0, 0, 1),
    )
    shell = cq.Workplane("XY").add(outer_cone).cut(cq.Workplane("XY").add(inner_cone))

    clip_span = outer_r + follower_boss + 10.0
    clip_height = height + tab_ext + 4.0
    # Use a solid cutter to remove the unwanted half instead of Workplane.intersect();
    # this avoids coincident-face kernel issues near the X=0 split plane.
    if side == "left":
        half_cutter = cq.Solid.makeBox(
            clip_span + 2.0,
            clip_span * 2.0 + 4.0,
            clip_height,
            pnt=cq.Vector(0.0, -clip_span - 2.0, -2.0),
        )
    else:
        half_cutter = cq.Solid.makeBox(
            clip_span + 2.0,
            clip_span * 2.0 + 4.0,
            clip_height,
            pnt=cq.Vector(-clip_span - 2.0, -clip_span - 2.0, -2.0),
        )
    shell = shell.cut(cq.Workplane("XY").add(half_cutter))

    # Tip-block relief: clear the nominal insert envelope from the shell apex region.
    tip_block_relief = cq.Solid.makeBox(
        params.TIP_BLOCK_WIDTH_MM,
        params.TIP_BLOCK_DEPTH_MM,
        params.TIP_BLOCK_HEIGHT_MM,
        pnt=cq.Vector(
            -params.TIP_BLOCK_WIDTH_MM / 2.0,
            -params.TIP_BLOCK_DEPTH_MM / 2.0,
            0.0,
        ),
    )
    shell = shell.cut(cq.Workplane("XY").add(tip_block_relief))

    tab = (
        cq.Workplane("XY")
        .box(follower_boss / 2.0, follower_boss, tab_ext, centered=(False, True, False))
        .translate(((-follower_boss / 2.0 if side == "left" else 0.0), 0.0, height))
    )
    shell = shell.union(tab)

    follower_bore = cq.Solid.makeCylinder(
        params.SHELL_FOLLOWER_BORE_DIA_MM / 2.0,
        tab_ext + 4.0,
        pnt=cq.Vector(side_sign * (follower_boss / 4.0), 0.0, height - 2.0),
        dir=cq.Vector(0.0, 0.0, 1.0),
    )
    shell = shell.cut(cq.Workplane("XY").add(follower_bore))

    hinge_bore = cq.Solid.makeCylinder(
        params.TIP_HINGE_BORE_DIA_MM / 2.0,
        follower_boss + 4.0,
        pnt=cq.Vector((-follower_boss - 2.0 if side == "left" else 0.0), 0.0, params.TIP_HINGE_BORE_Z_MM),
        dir=cq.Vector(1.0, 0.0, 0.0),
    )
    shell = shell.cut(cq.Workplane("XY").add(hinge_bore))

    if include_fin_slot:
        slot_length = min(params.FIN_SLOT_LENGTH_MM, height + tab_ext)
        fin_slot_solid = cq.Solid.makeBox(
            params.FIN_SLOT_DEPTH_MM + 0.01,
            params.FIN_SLOT_WIDTH_MM,
            slot_length,
            pnt=cq.Vector(-0.01, -params.FIN_SLOT_WIDTH_MM / 2.0, 0.0),
        )
        shell = shell.cut(cq.Workplane("XY").add(fin_slot_solid))

    split_face = ">X" if side == "left" else "<X"
    try:
        shell = shell.faces(split_face).edges().chamfer(params.SHELL_SEAM_RELIEF_CHAMFER_MM)
    except Exception:
        pass

    return shell
