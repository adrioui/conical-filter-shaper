"""
Sliding Arm — Universal Filter Ruler
=======================================
One of two identical arms that slide along the T-slot rails.
  - 150mm × 25mm × 6mm aluminum bar
  - T-slot engagement tab (5mm deep)
  - Raised fold-guide edge (R1.5mm rounded)
  - R2mm comfort radius on all external edges
  - Vernier scale laser-etched on top face (0.5° resolution)
  - Cam slot for cam-lock engagement

Material: 6061-T6 Aluminum, Type III hard anodized
Qty per assembly: 2 (left and right, mirrored geometry)
Spec ref: docs/design_spec.md § Sliding Arms

Coordinate System
-----------------
- Origin: Pivot end (cam lock hole end)
- X-axis: Along arm length (extends away from pivot)
- Y-axis: Lateral (fold guide on +Y side for left arm)
- Z-axis: Up (top face at +Z)
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

from cad.params import (
    ARM_LENGTH_MM,
    ARM_WIDTH_MM,
    ARM_THICKNESS_MM,
    ARM_EDGE_RADIUS_MM,
    ARM_FOLD_GUIDE_HEIGHT_MM,
    ARM_FOLD_GUIDE_PROFILE_MM,
    ARM_TSLOT_ENGAGEMENT_MM,
    TSLOT_OPENING_MM,
    TSLOT_UNDERCUT_MM,
    TSLOT_DEPTH_MM,
)


def build(params=None, side: str = "left") -> "cq.Workplane":
    """
    Build one sliding arm solid.

    Parameters
    ----------
    params : module, optional
        The cad.params module (for consistent parameter access). If None,
        constants are imported directly.
    side : str
        Which arm: "left" or "right". Determines fold guide edge orientation.
        - "left": fold guide on the +Y edge
        - "right": fold guide on the -Y edge (mirrored)

    Returns
    -------
    cq.Workplane
        A CadQuery workplane containing the sliding arm solid.

    Geometry
    --------
    - Rectangular bar: ARM_LENGTH_MM × ARM_WIDTH_MM × ARM_THICKNESS_MM
    - Origin: At pivot end (cam lock hole end), center-bottom
    - T-slot tongue: ARM_TSLOT_ENGAGEMENT_MM deep, fits into T-slot opening
    - Raised fold guide: ARM_FOLD_GUIDE_HEIGHT_MM high, rounded top
    - R2mm edge fillets on all external edges
    - Elongated cam slot for position adjustment
    """
    if cq is None:
        raise ImportError("CadQuery is required for sliding_arm.build()")

    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")

    # Use params if provided, otherwise use imported constants
    if params is not None:
        length = params.ARM_LENGTH_MM
        width = params.ARM_WIDTH_MM
        thickness = params.ARM_THICKNESS_MM
        edge_radius = params.ARM_EDGE_RADIUS_MM
        guide_height = params.ARM_FOLD_GUIDE_HEIGHT_MM
        guide_profile = params.ARM_FOLD_GUIDE_PROFILE_MM
        engagement_depth = params.ARM_TSLOT_ENGAGEMENT_MM
        tslot_opening = params.TSLOT_OPENING_MM
        tslot_undercut = params.TSLOT_UNDERCUT_MM
    else:
        length = ARM_LENGTH_MM
        width = ARM_WIDTH_MM
        thickness = ARM_THICKNESS_MM
        edge_radius = ARM_EDGE_RADIUS_MM
        guide_height = ARM_FOLD_GUIDE_HEIGHT_MM
        guide_profile = ARM_FOLD_GUIDE_PROFILE_MM
        engagement_depth = ARM_TSLOT_ENGAGEMENT_MM
        tslot_opening = TSLOT_OPENING_MM
        tslot_undercut = TSLOT_UNDERCUT_MM

    # ── Create main arm body with fillets FIRST ────────────────────────────────
    # Origin at pivot end, center of bottom face
    # Arm extends in +X direction, centered on Y

    arm = (
        cq.Workplane("XY")
        .box(length, width, thickness, centered=(False, True, False))
        # Apply fillets to main body edges
        .edges("|X").fillet(edge_radius)
        .edges("|Z").fillet(edge_radius)
    )

    # ── T-slot engagement tongue ───────────────────────────────────────────────
    # Fits into the T-slot rail on the base plate
    # Tongue protrudes from bottom of arm

    tongue_width = tslot_opening - 0.2
    tongue_length = length - 30
    tongue_start = 15

    tongue = (
        cq.Workplane("XY")
        .transformed(offset=(tongue_start + tongue_length / 2, 0, -engagement_depth / 2))
        .box(tongue_length, tongue_width, engagement_depth, centered=(True, True, False))
    )

    arm = arm.union(tongue.val())

    # ── Raised fold guide edge ─────────────────────────────────────────────────
    # Raised ridge along one long side for filter paper alignment

    guide_width = 4.0
    guide_length = length - 20

    # Position fold guide on appropriate side
    if side == "left":
        guide_y_offset = (width / 2) + (guide_width / 2)  # +Y side
    else:
        guide_y_offset = -(width / 2) - (guide_width / 2)  # -Y side

    fold_guide = (
        cq.Workplane("XY")
        .transformed(
            offset=(10 + guide_length / 2, guide_y_offset, thickness + guide_height / 2)
        )
        .box(guide_length, guide_width, guide_height, centered=(True, True, False))
        .edges("|X").fillet(guide_profile)  # Round the guide edges
    )

    arm = arm.union(fold_guide.val())

    # ── Cam lock slot ─────────────────────────────────────────────────────────
    # Elongated slot near the pivot end for cam lock engagement

    slot_width = 5.4  # M5 clearance hole
    slot_length = 15
    slot_x_pos = 20

    cam_slot = (
        cq.Workplane("XY")
        .transformed(offset=(slot_x_pos, 0, -engagement_depth / 2))
        .slot2D(slot_length, slot_width, angle=0)
        .extrude(thickness + engagement_depth + 1)
    )

    arm = arm.cut(cam_slot.val())

    return arm


def build_assembly(params=None) -> "cq.Workplane":
    """
    Build both left and right arms for reference.

    Returns
    -------
    cq.Workplane
        Assembly containing both arms positioned correctly.
    """
    if cq is None:
        raise ImportError("CadQuery is required for sliding_arm.build_assembly()")

    left_arm = build(params=params, side="left")
    right_arm = build(params=params, side="right")

    # Mirror right arm across Y-axis
    right_arm = right_arm.mirror("YZ")

    # Combine into assembly
    assembly = cq.Assembly()
    assembly.add(left_arm.val(), name="left_arm")
    assembly.add(right_arm.val(), name="right_arm")

    return assembly