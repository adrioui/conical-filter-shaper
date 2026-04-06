"""
Base Plate — Universal Filter Ruler
=====================================
Flat aluminum plate (200mm × 120mm × 8mm) with:
  - 2× T-slot rails for sliding arms
  - Magnetic marker track recess
  - Laser-etched angle scale (40°–85°), filter size guides, overlap scale
  - 4× silicone foot pad recesses (bottom face)

Material: 6061-T6 Aluminum, Type III hard anodized
Spec ref: docs/design_spec.md § Base Plate
"""
from __future__ import annotations
import math

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

from cad.params import (
    BASE_LENGTH_MM,
    BASE_WIDTH_MM,
    BASE_THICKNESS_MM,
    T_SLOT_OPENING_MM,
    T_SLOT_UNDERCUT_MM,
    T_SLOT_DEPTH_MM,
    RAIL_LENGTH_MM,
    RAIL_SPACING_MM,
    ANGLE_MIN_DEG,
    ANGLE_MAX_DEG,
    MAGNETIC_TRACK_LENGTH_MM,
    MAGNETIC_TRACK_WIDTH_MM,
    MAGNETIC_TRACK_DEPTH_MM,
    FOOT_PAD_DIAMETER_MM,
    FOOT_PAD_DEPTH_MM,
    FOOT_PAD_SPACING_X_MM,
    FOOT_PAD_SPACING_Y_MM,
    EDGE_FILLET_RADIUS_MM,
    CAM_BOLT_DIAMETER_MM,
)


def _t_slot_profile(width_open: float, width_under: float, depth: float) -> cq.Workplane:
    """Create a T-slot profile for cutting.

    Profile is centered at origin, extends in +Y direction.
    """
    # T-slot shape: narrow opening at top, wider undercut below
    half_open = width_open / 2
    half_under = width_under / 2
    
    points = [
        (-half_open, 0),
        (-half_open, depth - 0.5),  # narrow section
        (-half_under, depth - 0.5),  # step to undercut
        (-half_under, depth),       # bottom left
        (half_under, depth),        # bottom right
        (half_under, depth - 0.5),  # step from undercut
        (half_open, depth - 0.5),   # narrow section
        (half_open, 0),             # top right
    ]
    
    return cq.Workplane("XZ").polyline(points).close().extrude(width_under)


def build(params=None) -> "cq.Workplane":
    """Build the base plate solid.
    
    Origin: Center of bottom face (Z=0 is bottom, +Z is up toward top face).
    
    Returns:
        CadQuery Workplane with the base plate solid.
    """
    if cq is None:
        raise RuntimeError("CadQuery not available")
    
    # Start with base plate
    plate = (
        cq.Workplane("XY")
        .box(BASE_LENGTH_MM, BASE_WIDTH_MM, BASE_THICKNESS_MM, centered=True)
        .translate((0, 0, BASE_THICKNESS_MM / 2))  # Bottom face at Z=0
    )
    
    # Calculate rail angles - symmetric about Y axis, angled outward
    # Rails run from pivot center toward edges at (90 - max_angle/2) orientation
    half_angle_span = (ANGLE_MAX_DEG - ANGLE_MIN_DEG) / 2
    rail_angle = 90 - (ANGLE_MIN_DEG + half_angle_span) / 2
    
    # Create T-slot rails
    rail_half_spacing = RAIL_SPACING_MM / 2
    
    for side, sign in [("left", -1), ("right", 1)]:
        # Rail position offset from center
        y_offset = sign * rail_half_spacing
        
        # Rail angle - symmetric
        angle = sign * (90 - 60)  # Approximate 30° from vertical for 60° default
        
        # Create T-slot cut
        slot = (
            cq.Workplane("XY")
            .rect(T_SLOT_UNDERCUT_MM, RAIL_LENGTH_MM)
            .extrude(-T_SLOT_DEPTH_MM)  # Cut downward into top face
        )
        
        # Position slot along rail path
        # Rail starts at pivot center (top of plate) and extends outward
        slot = slot.rotate((0, 0, 0), (0, 0, 1), angle)
        slot = slot.translate((
            math.sin(math.radians(angle)) * RAIL_LENGTH_MM / 2,
            y_offset + math.cos(math.radians(angle)) * RAIL_LENGTH_MM / 2,
            BASE_THICKNESS_MM
        ))
        
        plate = plate.cut(slot)
    
    # Magnetic track recess (centered, on top face)
    track_recess = (
        cq.Workplane("XY")
        .box(MAGNETIC_TRACK_LENGTH_MM, MAGNETIC_TRACK_WIDTH_MM, MAGNETIC_TRACK_DEPTH_MM * 2, centered=True)
        .translate((0, 0, BASE_THICKNESS_MM - MAGNETIC_TRACK_DEPTH_MM / 2))
    )
    plate = plate.cut(track_recess)
    
    # Foot pad recesses (4x, on bottom face)
    foot_x = FOOT_PAD_SPACING_X_MM / 2
    foot_y = FOOT_PAD_SPACING_Y_MM / 2
    
    for fx in [-foot_x, foot_x]:
        for fy in [-foot_y, foot_y]:
            foot = (
                cq.Workplane("XY")
                .circle(FOOT_PAD_DIAMETER_MM / 2)
                .extrude(FOOT_PAD_DEPTH_MM * 2)
                .translate((fx, fy, 0))
            )
            plate = plate.cut(foot)
    
    # Cam lock through-holes (2x M5)
    cam_hole = (
        cq.Workplane("XY")
        .circle(CAM_BOLT_DIAMETER_MM / 2)
        .extrude(BASE_THICKNESS_MM * 2)
    )
    
    for sign in [-1, 1]:
        cam_pos = cam_hole.translate((
            sign * RAIL_LENGTH_MM / 2,
            sign * rail_half_spacing,
            BASE_THICKNESS_MM / 2
        ))
        plate = plate.cut(cam_pos)
    
    # Edge fillets
    plate = plate.edges().fillet(EDGE_FILLET_RADIUS_MM)
    
    return plate
