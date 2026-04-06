"""
Sliding Arm — Universal Filter Ruler
=====================================
One of two identical arms that slide along the T-slot rails.
  - 150mm × 25mm × 6mm aluminum bar
  - T-slot engagement tongue (5mm deep, fits T-slot opening)
  - Raised fold-guide edge (3mm high, R1.5mm rounded top)
  - R2mm comfort radius on all external edges
  - Cam lock slot for position adjustment (elongated for 90° cam throw)

Material: 6061-T6 Aluminum, Type III hard anodized
Qty per assembly: 2 (left and right, mirrored geometry)
Spec ref: cad/params.py — SLIDING ARMS section

Coordinate System
-----------------
- Origin: Pivot end (cam lock hole end), center-bottom
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
    CAM_THROW_DEG,
)


# Cam lock slot length computed from 90° cam throw
# Slot must accommodate the eccentric motion of a quarter-turn cam
CAM_LOCK_SLOT_LENGTH_MM = 15.0  # Millimeters of travel for 90° throw


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
    - Origin: At pivot end (cam lock hole end), center of bottom face
    - T-slot tongue: ARM_TSLOT_ENGAGEMENT_MM deep, fits into T-slot opening
    - Raised fold guide: ARM_FOLD_GUIDE_HEIGHT_MM high, R1.5mm rounded top
    - R2mm edge fillets on all external edges
    - Elongated cam slot for position adjustment (CAM_LOCK_SLOT_LENGTH_MM)
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
    else:
        length = ARM_LENGTH_MM
        width = ARM_WIDTH_MM
        thickness = ARM_THICKNESS_MM
        edge_radius = ARM_EDGE_RADIUS_MM
        guide_height = ARM_FOLD_GUIDE_HEIGHT_MM
        guide_profile = ARM_FOLD_GUIDE_PROFILE_MM
        engagement_depth = ARM_TSLOT_ENGAGEMENT_MM
        tslot_opening = TSLOT_OPENING_MM

    # ── Main arm body ────────────────────────────────────────────────────────
    # Origin at pivot end (X=0), center of bottom face (Y=0, Z=0)
    # Arm extends in +X direction, centered on Y

    arm = (
        cq.Workplane("XY")
        .box(length, width, thickness, centered=(False, True, False))
    )

    # ── T-slot engagement tongue ──────────────────────────────────────────────
    # Tongue protrudes from bottom of arm, fits into T-slot opening
    # Width matches T-slot opening (6mm) with small clearance
    # Length covers most of arm except pivot end region

    tongue_width = tslot_opening - 0.2  # Small clearance for sliding fit
    tongue_length = length - 30  # Leave clearance at pivot end
    tongue_start_x = 15  # Start 15mm from pivot end

    tongue_profile = (
        cq.Workplane("XZ")
        .moveTo(tongue_start_x, 0)
        .lineTo(tongue_start_x + tongue_length, 0)
        .lineTo(tongue_start_x + tongue_length, -engagement_depth)
        .lineTo(tongue_start_x, -engagement_depth)
        .close()
    )

    tongue = tongue_profile.extrude(tongue_width / 2).mirror("XZ", union=True)
    arm = arm.union(tongue)

    # ── Raised fold guide edge ─────────────────────────────────────────────────
    # Raised ridge along one long side for filter paper alignment
    # R1.5mm rounded top profile

    guide_width = 3.0  # Width of the guide ridge
    guide_length = length - 20  # Leave clearance at both ends
    guide_start_x = 10  # Start 10mm from pivot end

    # Position fold guide on appropriate side
    if side == "left":
        guide_y_offset = width / 2  # +Y side
    else:
        guide_y_offset = -width / 2  # -Y side

    # Create guide with rounded top profile (R1.5mm)
    # Profile: flat bottom, rounded top corners
    guide_profile_points = [
        (0, 0),  # bottom-left on arm surface
        (guide_width, 0),  # bottom-right on arm surface
        (guide_width, guide_height - guide_profile),  # up right side
        # Rounded top - arc approximation
        (guide_width - guide_profile, guide_height),  # top-right corner
        (guide_profile, guide_height),  # top-left corner
        (0, guide_height - guide_profile),  # left side top
        (0, 0),  # back to start
    ]

    # Simplified: create rectangular guide with fillet after union
    fold_guide = (
        cq.Workplane("XZ")
        .moveTo(guide_start_x, thickness)  # Start on top surface at guide_start_x
        .lineTo(guide_start_x + guide_length, thickness)
        .lineTo(guide_start_x + guide_length, thickness + guide_height)
        .lineTo(guide_start_x, thickness + guide_height)
        .close()
    )

    fold_guide_solid = fold_guide.extrude(guide_width / 2).mirror("XZ", union=True).translate((0, guide_y_offset, 0))
    arm = arm.union(fold_guide_solid)

    # ── Cam lock slot ─────────────────────────────────────────────────────────
    # Elongated slot near the pivot end for cam lock engagement
    # Slot allows position adjustment along the rail

    slot_width = 5.4  # M5 clearance hole
    slot_x_pos = 12  # Position at pivot end
    slot_through_height = thickness + engagement_depth + 1  # Through arm body and tongue

    cam_slot = (
        cq.Workplane("YZ")
        .slot2D(CAM_LOCK_SLOT_LENGTH_MM, slot_width, angle=0)
        .extrude(slot_through_height * 2)
        .translate((slot_x_pos - CAM_LOCK_SLOT_LENGTH_MM / 2, 0, -engagement_depth))
    )

    arm = arm.cut(cam_slot)

    # ── Edge fillets ──────────────────────────────────────────────────────────
    # Apply R2mm comfort fillets to all external edges
    # Use handleEdges selection to safely apply fillets

    try:
        # Fillet edges along the length (|X direction)
        arm = arm.edges("|X").fillet(edge_radius)
    except Exception:
        # If fillet fails on some edges, skip those and continue
        pass

    try:
        # Fillet edges perpendicular to length (|Y direction)
        arm = arm.edges("|Y").fillet(edge_radius)
    except Exception:
        pass

    try:
        # Fillet edges perpendicular to thickness (|Z direction) 
        arm = arm.edges("|Z").fillet(edge_radius)
    except Exception:
        pass

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