"""
Universal Filter Ruler — Design Parameters
==========================================
Single source of truth for ALL dimensions, tolerances, and material specs
for the Universal Coffee Filter Ruler (flat adjustable ruler).

Rules
-----
- All lengths in mm unless the name ends with a different unit suffix.
- All angles in degrees; included angle unless named *_half_angle*.
- Every constant in this file is referenced at least once in cad/components/ or tests/.
- Do NOT hardcode numbers in component files — always import from here.

Revision: 1.0  (bump via scripts/bump_revision.py)
Spec reference:
  vault/Design Specifications.md
  vault/CAD Design Brief.md
  vault/Bill of Materials.md
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Final

# ── Revision ──────────────────────────────────────────────────────────────────
REVISION: Final[str] = "1.0"


# ═══════════════════════════════════════════════════════════════════════════════
# RULER PRESETS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class RulerPreset:
    """
    Named configuration for the Universal Filter Ruler.

    Attributes
    ----------
    name : str
        Human-readable preset name (e.g. "Standard", "Travel").
    base_length_mm : float
        Overall length of the base plate (mm).
    base_width_mm : float
        Overall width of the base plate (mm).
    base_thickness_mm : float
        Thickness of the base plate (mm).
    weight_g : float
        Approximate assembled weight (grams).
    folded_height_mm : float
        Total stacked height when arms are folded flat (mm).
    """
    name: str
    base_length_mm: float
    base_width_mm: float
    base_thickness_mm: float
    weight_g: float
    folded_height_mm: float


STANDARD_PRESET: Final[RulerPreset] = RulerPreset(
    name="Standard",
    base_length_mm=200.0,
    base_width_mm=120.0,
    base_thickness_mm=8.0,
    weight_g=350.0,
    folded_height_mm=15.0,
)

TRAVEL_PRESET: Final[RulerPreset] = RulerPreset(
    name="Travel",
    base_length_mm=150.0,
    base_width_mm=90.0,
    base_thickness_mm=8.0,
    weight_g=250.0,
    folded_height_mm=15.0,
)

RULER_PRESETS: Final[list[RulerPreset]] = [STANDARD_PRESET, TRAVEL_PRESET]
DEFAULT_RULER_PRESET: Final[RulerPreset] = STANDARD_PRESET


# ═══════════════════════════════════════════════════════════════════════════════
# BASE PLATE  (part: base_plate.py)
# ═══════════════════════════════════════════════════════════════════════════════

BASE_LENGTH_MM: Final[float] = 200.0          # Standard version; see STANDARD_PRESET
BASE_WIDTH_MM: Final[float] = 120.0
BASE_THICKNESS_MM: Final[float] = 8.0
BASE_FLATNESS_MM: Final[float] = 0.05         # Over full 200 mm length

BASE_MATERIAL: Final[str] = "6061-T6 Aluminum"
BASE_PROCESS: Final[str] = "CNC milled → deburr → anodize → laser etch → paint fill"
BASE_SURFACE_TREATMENT: Final[str] = "Type III hard anodize — space grey or matte black"
BASE_COLOR_OPTIONS: Final[list[str]] = ["Space Grey", "Matte Black"]
BASE_SURFACE_FINISH_PRE_ANODIZE: Final[str] = "Bead blasted"


# ═══════════════════════════════════════════════════════════════════════════════
# T-SLOT RAILS  (machined into base plate; qty: 2)
# ═══════════════════════════════════════════════════════════════════════════════

TSLOT_COUNT: Final[int] = 2
TSLOT_OPENING_MM: Final[float] = 6.0          # Slot width at top face
TSLOT_UNDERCUT_MM: Final[float] = 10.0        # Undercut width (wide part)
TSLOT_DEPTH_MM: Final[float] = 5.0            # Slot depth into base
TSLOT_LENGTH_MM: Final[float] = 180.0
TSLOT_FIT_CLASS: Final[str] = "H7/h6 sliding fit"
TSLOT_WIDTH_TOL_MM: Final[float] = 0.02       # +0.02 / -0.00 on opening width
TSLOT_DEPTH_TOL_MM: Final[float] = 0.05
TSLOT_SURFACE_FINISH_RA_UM: Final[float] = 0.8


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDING ARMS  (part: sliding_arm.py; qty: 2)
# ═══════════════════════════════════════════════════════════════════════════════

ARM_COUNT: Final[int] = 2
ARM_LENGTH_MM: Final[float] = 150.0
ARM_WIDTH_MM: Final[float] = 25.0
ARM_THICKNESS_MM: Final[float] = 6.0
ARM_EDGE_RADIUS_MM: Final[float] = 2.0        # Comfort rounding on all external edges
ARM_FOLD_GUIDE_HEIGHT_MM: Final[float] = 3.0  # Raised fold-guide ridge (top face)
ARM_FOLD_GUIDE_PROFILE_MM: Final[float] = 1.5 # Rounded top of guide (R1.5 mm)
ARM_TSLOT_ENGAGEMENT_MM: Final[float] = 5.0   # Depth of T-tab into slot
ARM_WIDTH_TOL_MM: Final[float] = 0.05
ARM_THICKNESS_TOL_MM: Final[float] = 0.05
ARM_ENGAGEMENT_TOL_MM: Final[float] = 0.02    # Critical: ±0.02 mm

ARM_MATERIAL: Final[str] = "6061-T6 Aluminum"
ARM_PROCESS: Final[str] = "CNC milled → deburr → anodize → laser etch"
ARM_SURFACE_TREATMENT: Final[str] = "Type III hard anodize — space grey"


# ═══════════════════════════════════════════════════════════════════════════════
# ANGLE MEASUREMENT SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

# Operating range
ANGLE_MIN_DEG: Final[float] = 40.0            # Narrowest setting
ANGLE_MAX_DEG: Final[float] = 85.0            # Widest setting
ANGLE_RANGE_DEG: Final[float] = ANGLE_MAX_DEG - ANGLE_MIN_DEG  # = 45°

# Primary scale (laser etched on base plate)
ANGLE_PRIMARY_TICK_DEG: Final[float] = 1.0    # Minor tick spacing
ANGLE_MAJOR_TICK_DEG: Final[float] = 5.0      # Major (labeled) tick spacing
ANGLE_SCALE_METHOD: Final[str] = "Laser etched, black paint fill"
ANGLE_SCALE_CONTRAST: Final[str] = "Black filled on silver/grey base"
ANGLE_ACCURACY_DEG: Final[float] = 0.1        # ±0.1° verification at QC

# Vernier scale (laser etched on sliding arm)
ANGLE_VERNIER_RESOLUTION_DEG: Final[float] = 0.5
ANGLE_VERNIER_LENGTH_MM: Final[float] = 30.0  # Physical length of vernier window
ANGLE_VERNIER_LOCATION: Final[str] = "On sliding arm edge, adjacent to base scale"

# Geometry: arms pivot symmetrically from a common origin
ANGLE_PIVOT_LOCATION: Final[str] = "Center-top of base plate"
ANGLE_MEASUREMENT_TYPE: Final[str] = "Included angle between arm inner edges"


# ═══════════════════════════════════════════════════════════════════════════════
# CAM LOCK MECHANISM  (part: cam_lock.py; qty: 2)
# ═══════════════════════════════════════════════════════════════════════════════

CAM_COUNT: Final[int] = 2
CAM_TYPE: Final[str] = "Eccentric cam lock"
CAM_THROW_DEG: Final[float] = 90.0            # Quarter-turn to lock/unlock
CAM_LEVER_LENGTH_MM: Final[float] = 25.0
CAM_BOLT_SPEC: Final[str] = "M5 shoulder bolt, SS 316"
CAM_CLAMP_FORCE_N: Final[float] = 50.0        # Minimum holding force when locked
CAM_MATERIAL: Final[str] = "Stainless Steel 316 — passivated"
CAM_LEVER_MATERIAL: Final[str] = "6061-T6 Aluminum — Type III hard anodize, matte black"
CAM_OPERATION: Final[str] = "Single-handed, quarter-turn, positive lock indication"
CAM_FIELD_REPLACEABLE: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════════
# MAGNETIC PRESET MARKERS  (part: magnetic_marker.py)
# ═══════════════════════════════════════════════════════════════════════════════

MARKER_COUNT: Final[int] = 8                  # Total: 4 colors × 2 each
MARKER_COLOR_COUNT: Final[int] = 4
MARKER_COLORS: Final[list[str]] = ["Red", "Blue", "Green", "Yellow"]
MARKER_PER_COLOR: Final[int] = 2

MARKER_DIAMETER_MM: Final[float] = 6.0
MARKER_HEIGHT_MM: Final[float] = 4.0
MARKER_MAGNET_GRADE: Final[str] = "N52"       # Neodymium N52
MARKER_PULL_FORCE_KG: Final[float] = 0.5      # Minimum retention force (≥ 0.5 kg)
MARKER_MATERIAL: Final[str] = "Anodized 6061-T6 aluminum housing + N52 neodymium magnet"
MARKER_PROCESS: Final[str] = "CNC turned housing, press-fit magnet + adhesive backup"

# Internal magnet dimensions (inside the 6×4mm housing)
MARKER_MAGNET_DIAMETER_MM: Final[float] = 5.0   # Ø5×2mm N52 neodymium
MARKER_MAGNET_THICKNESS_MM: Final[float] = 2.0

# Magnetic track (recess in base plate that accepts markers)
MARKER_TRACK_LENGTH_MM: Final[float] = 180.0
MARKER_TRACK_WIDTH_MM: Final[float] = 8.0
MARKER_TRACK_RECESS_DEPTH_MM: Final[float] = 1.0
MARKER_TRACK_INSERT_SPEC: Final[str] = "Mild steel strip 180×6×1 mm, zinc plated"
MARKER_TRACK_CAPACITY: Final[int] = 8


# ═══════════════════════════════════════════════════════════════════════════════
# FILTER SIZE GUIDE CIRCLES  (etched on base plate top face)
# ═══════════════════════════════════════════════════════════════════════════════

# Radii for the three standard filter sizes (dashed-arc outlines)
FILTER_01_RADIUS_MM: Final[float] = 55.0      # 01 size — Ø110mm
FILTER_02_RADIUS_MM: Final[float] = 77.5      # 02 size — Ø155mm
FILTER_03_RADIUS_MM: Final[float] = 92.5      # 03 size — Ø185mm

FILTER_GUIDES: Final[dict[str, float]] = {
    "01": FILTER_01_RADIUS_MM,
    "02": FILTER_02_RADIUS_MM,
    "03": FILTER_03_RADIUS_MM,
}

FILTER_GUIDE_LINE_WIDTH_MM: Final[float] = 0.3
FILTER_GUIDE_STYLE: Final[str] = "Dashed laser-etched arc, labeled 01 / 02 / 03"
FILTER_GUIDE_CENTER: Final[str] = "Cross-hair at arm pivot origin, 1mm line width, 10mm length"


# ═══════════════════════════════════════════════════════════════════════════════
# OVERLAP MEASUREMENT SCALE  (etched on right side of base)
# ═══════════════════════════════════════════════════════════════════════════════

OVERLAP_SCALE_MIN_MM: Final[float] = 0.0
OVERLAP_SCALE_MAX_MM: Final[float] = 20.0
OVERLAP_SCALE_TICK_MM: Final[float] = 1.0           # Every 1mm
OVERLAP_SCALE_LABEL_INTERVAL_MM: Final[float] = 5.0 # Numbers every 5mm
OVERLAP_SCALE_LOCATION: Final[str] = "Right side of base plate"
OVERLAP_SCALE_TYPE: Final[str] = "Etched scale with numbers every 5mm"


# ═══════════════════════════════════════════════════════════════════════════════
# PTFE SLIDE STRIPS  (part: ptfe_slide_strip.py; qty: 2)
# ═══════════════════════════════════════════════════════════════════════════════

PTFE_COUNT: Final[int] = 2
PTFE_LENGTH_MM: Final[float] = 180.0
PTFE_WIDTH_MM: Final[float] = 6.0
PTFE_THICKNESS_MM: Final[float] = 0.5
PTFE_MATERIAL: Final[str] = "PTFE (polytetrafluoroethylene)"
PTFE_PURPOSE: Final[str] = "Ultra-smooth arm sliding in T-slot"


# ═══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY HARDWARE  (bought-in; BOM reference)
# ═══════════════════════════════════════════════════════════════════════════════

FASTENER_M3_SHCS_SPEC: Final[str] = "M3×8 SHCS, SS A2-70"
FASTENER_M3_SHCS_QTY: Final[int] = 4

FASTENER_M5_SHOULDER_SPEC: Final[str] = "M5 shoulder bolt, SS 316"
FASTENER_M5_SHOULDER_QTY: Final[int] = 2

FASTENER_BELLEVILLE_SPEC: Final[str] = "Belleville washer M5, spring steel"
FASTENER_BELLEVILLE_QTY: Final[int] = 2

# Anti-slip foot pads (bottom face of base plate)
FOOT_PAD_COUNT: Final[int] = 4
FOOT_PAD_DIAMETER_MM: Final[float] = 8.0
FOOT_PAD_THICKNESS_MM: Final[float] = 1.5
FOOT_PAD_RECESS_DEPTH_MM: Final[float] = 0.5  # Recessed into base (adhesive mount)
FOOT_PAD_MATERIAL: Final[str] = "Silicone, adhesive-backed"


# ═══════════════════════════════════════════════════════════════════════════════
# TOLERANCES  (critical dimensions — 100% inspection)
# ═══════════════════════════════════════════════════════════════════════════════

TOL_TSLOT_WIDTH_MM: Final[float] = 0.02       # +0.02 / -0.00 on slot opening
TOL_TSLOT_DEPTH_MM: Final[float] = 0.05
TOL_TSLOT_UNDERCUT_MM: Final[float] = 0.05
TOL_ARM_WIDTH_MM: Final[float] = 0.05
TOL_ARM_THICKNESS_MM: Final[float] = 0.05
TOL_ARM_ENGAGEMENT_MM: Final[float] = 0.02    # T-tab depth critical tolerance
TOL_ANGLE_SCALE_DEG: Final[float] = 0.1       # ±0.1° angle accuracy
TOL_MAGNETIC_TRACK_SPACING_MM: Final[float] = 0.1
TOL_FLATNESS_MM: Final[float] = 0.05          # Over 200mm full base length
TOL_LINEAR_MM: Final[float] = 0.1             # General linear dimensions
TOL_ANGULAR_DEG: Final[float] = 0.5           # General angular dimensions
TOL_SURFACE_FINISH_RA_UM: Final[float] = 0.8  # Functional surfaces


# ═══════════════════════════════════════════════════════════════════════════════
# MATERIAL PROPERTIES  (reference; for BOM and drawing annotations)
# ═══════════════════════════════════════════════════════════════════════════════

# 6061-T6 Aluminum
AL6061_TENSILE_STRENGTH_MPA: Final[float] = 290.0
AL6061_YIELD_STRENGTH_MPA: Final[float] = 240.0
AL6061_DENSITY_G_CM3: Final[float] = 2.7
AL6061_MACHINABILITY: Final[str] = "Excellent"
AL6061_ANODIZING: Final[str] = "Good anodizing characteristics"

# Type III Hard Anodize
ANODIZE_TYPE_III_THICKNESS_UM: Final[tuple[float, float]] = (25.0, 50.0)  # min, max
ANODIZE_TYPE_III_HARDNESS_HRC: Final[tuple[float, float]] = (60.0, 70.0)
ANODIZE_TYPE_III_WEAR_RESISTANCE: Final[str] = "Excellent"
ANODIZE_TYPE_III_CORROSION_RESISTANCE: Final[str] = "Excellent"

# Stainless Steel 316
SS316_MATERIAL: Final[str] = "Stainless Steel 316 — passivated"
SS316_APPLICATION: Final[str] = "Cam bodies, shoulder bolts — corrosion resistant"

# Finish matrix per component
FINISH_MATRIX: Final[dict[str, str]] = {
    "base_plate":   "6061-T6 Al / Type III hard anodize, space grey",
    "sliding_arm":  "6061-T6 Al / Type III hard anodize, space grey",
    "cam_body":     "SS 316 / passivated",
    "cam_lever":    "6061-T6 Al / Type III hard anodize, matte black",
    "marker":       "6061-T6 Al / Type II anodize, 4 colors",
    "ferrous_strip":"Mild steel / zinc plated",
}


# ═══════════════════════════════════════════════════════════════════════════════
# OVERALL TOOL ENVELOPE  (Standard version)
# ═══════════════════════════════════════════════════════════════════════════════

TOOL_BASE_LENGTH_MM: Final[float] = BASE_LENGTH_MM           # 200mm
TOOL_BASE_WIDTH_MM: Final[float] = BASE_WIDTH_MM             # 120mm
TOOL_TOTAL_HEIGHT_MM: Final[float] = BASE_THICKNESS_MM + ARM_THICKNESS_MM  # 14mm open
TOOL_FOLDED_HEIGHT_MM: Final[float] = STANDARD_PRESET.folded_height_mm    # 15mm
TOOL_MASS_ESTIMATE_G: Final[float] = STANDARD_PRESET.weight_g             # ~350g
