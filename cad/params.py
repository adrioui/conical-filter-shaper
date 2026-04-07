"""
Universal Coffee Filter Ruler v3.0 — Design Parameters
========================================================
Single source of truth for ALL dimensions, tolerances, and material specs
for the Universal Coffee Filter Ruler v3.0 bevel gauge design.

Product concept: Hinged V-shape filter ruler with tapered trapezoidal arms.
Two SS304 flat bar arms joined at a friction pivot, locked by thumb screw.
Bevel gauge style — the opening angle directly forms the cone angle of the filter.

v3.0 Changes from v2.0:
- Legs replaced with tapered trapezoidal arms (narrow pivot end, wide tip end)
- Fold marks replaced with arc groove marks at filter-specific radii
- Magnetic pivot removed (friction-only pivot)
- Travel preset removed (single standard preset)

Rules
-----
- All lengths in mm unless the name ends with a different unit suffix.
- All angles in degrees; included angle unless named *_half_angle*.
- Every constant in this file is referenced at least once in cad/components/ or tests/.
- Do NOT hardcode numbers in component files — always import from here.

Revision: 3.0  (bump via scripts/bump_revision.py)
"""

from __future__ import annotations
from typing import Final

# ── Revision ──────────────────────────────────────────────────────────────────
REVISION: Final[str] = "3.0"


# ═══════════════════════════════════════════════════════════════════════════════
# ARM GEOMETRY  (part: ruler_arm.py; qty: 2)
# ═══════════════════════════════════════════════════════════════════════════════
# Tapered trapezoidal arms — narrow at pivot end, wide at tip end

ARM_COUNT: Final[int] = 2
ARM_LENGTH_MM: Final[float] = 120.0           # Pivot hole center to tip
ARM_WIDTH_NARROW_MM: Final[float] = 25.0      # Width at pivot end (narrow)
ARM_WIDTH_WIDE_MM: Final[float] = 65.0        # Width at tip end (wide)
ARM_THICKNESS_MM: Final[float] = 1.2          # SS304 sheet thickness
ARM_EDGE_RADIUS_MM: Final[float] = 0.3        # R0.3mm deburred edges

# Pivot hole specification
ARM_PIVOT_HOLE_DIA_MM: Final[float] = 5.3     # M5 clearance hole
ARM_PIVOT_HOLE_OFFSET_MM: Final[float] = 10.0  # From narrow edge to hole center

# Material and finish
ARM_MATERIAL: Final[str] = "SS304 Stainless Steel"
ARM_SURFACE_FINISH: Final[str] = "#4 brushed finish"
ARM_PROCESS: Final[str] = "Laser cut → deburr → brush finish → laser etch"


# ═══════════════════════════════════════════════════════════════════════════════
# FILTER SIZE ARC MARKS  (laser etched grooves on arms)
# ═══════════════════════════════════════════════════════════════════════════════
# Radius measured from pivot hole center along the arm centerline.
# These correspond to the slant height of V60 filter sizes.

ARC_01_RADIUS_MM: Final[float] = 95.0         # V60-01 slant height
ARC_02_RADIUS_MM: Final[float] = 116.0        # V60-02 slant height
ARC_03_RADIUS_MM: Final[float] = 137.0        # V60-03 slant height

ARC_MARKS: Final[dict[str, float]] = {
    "01": ARC_01_RADIUS_MM,
    "02": ARC_02_RADIUS_MM,
    "03": ARC_03_RADIUS_MM,
}

ARC_GROOVE_WIDTH_MM: Final[float] = 0.3       # Laser etched groove width
ARC_GROOVE_DEPTH_MM: Final[float] = 0.1       # Shallow etch depth


# ═══════════════════════════════════════════════════════════════════════════════
# ANGLE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

# Operating range (opening angle of the V-shaped arms)
ANGLE_MIN_DEG: Final[float] = 40.0            # Narrowest setting
ANGLE_MAX_DEG: Final[float] = 85.0            # Widest setting
ANGLE_DEFAULT_DEG: Final[float] = 60.0        # Default V60 angle
ANGLE_RANGE_DEG: Final[float] = ANGLE_MAX_DEG - ANGLE_MIN_DEG  # = 45°

# Angle scale (laser etched ticks)
ANGLE_TICK_DEG: Final[float] = 1.0            # Minor tick spacing
ANGLE_LABEL_DEG: Final[float] = 5.0           # Major (labeled) tick spacing


# ═══════════════════════════════════════════════════════════════════════════════
# NAMED DRIPPER PRESETS  (common dripper opening angles)
# ═══════════════════════════════════════════════════════════════════════════════

DRIPPER_PRESETS: Final[dict[str, float]] = {
    "SD1R": 48.0,    # Small dripper 01R
    "SD1": 55.0,     # Small dripper 01
    "V60": 60.0,     # Hario V60 standard
    "UFO": 80.0,     # Kalita Wave 155 (flat-bottom)
}


# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT HARDWARE  (part: pivot_bolt.py; qty: 1)
# ═══════════════════════════════════════════════════════════════════════════════

PIVOT_BOLT_SPEC: Final[str] = "M5 shoulder bolt, SS316"
PIVOT_BOLT_DIAMETER_MM: Final[float] = 5.0    # M5 thread
PIVOT_SHOULDER_DIAMETER_MM: Final[float] = 8.0  # Shoulder section
PIVOT_SHOULDER_LENGTH_MM: Final[float] = 4.0  # Shoulder length
PIVOT_BOLT_HEAD_DIA_MM: Final[float] = 10.0   # Socket head diameter
PIVOT_BOLT_HEAD_HEIGHT_MM: Final[float] = 3.0 # Socket head height


# ═══════════════════════════════════════════════════════════════════════════════
# PTFE WASHER  (part: ptfe_washer.py; qty: 1)
# ═══════════════════════════════════════════════════════════════════════════════

WASHER_OD_MM: Final[float] = 10.0             # Outer diameter
WASHER_ID_MM: Final[float] = 5.3              # M5 clearance ID
WASHER_THICKNESS_MM: Final[float] = 0.5       # PTFE thickness


# ═══════════════════════════════════════════════════════════════════════════════
# THUMB SCREW  (part: thumb_screw.py; qty: 1)
# ═══════════════════════════════════════════════════════════════════════════════

THUMB_SCREW_HEAD_DIAMETER_MM: Final[float] = 15.0
THUMB_SCREW_HEAD_HEIGHT_MM: Final[float] = 8.0
THUMB_SCREW_SHAFT_DIAMETER_MM: Final[float] = 5.0
THUMB_SCREW_SHAFT_LENGTH_MM: Final[float] = 8.0
THUMB_SCREW_KNURL_COUNT: Final[int] = 12      # Diamond knurl pattern


# ═══════════════════════════════════════════════════════════════════════════════
# MATERIAL PROPERTIES  (SS304)
# ═══════════════════════════════════════════════════════════════════════════════

SS304_DENSITY_G_PER_CM3: Final[float] = 8.0   # Density for weight calc

# Weight estimates
# Arm area: trapezoid = (25+65)/2 × 120 = 5400mm² → 5400 × 1.2mm = 6480mm³
# 6480mm³ × 8g/cm³ = 51.84g per arm
ARM_WEIGHT_G: Final[float] = 51.8
TOTAL_WEIGHT_G: Final[float] = (
    ARM_WEIGHT_G * 2     # Two arms
    + 8                  # Pivot bolt & washer
    + 1                  # PTFE washer
    + 12                 # Thumb screw
)  # ≈ 125g total


# ═══════════════════════════════════════════════════════════════════════════════
# TOLERANCES
# ═══════════════════════════════════════════════════════════════════════════════

TOL_ARM_LENGTH_MM: Final[float] = 0.1         # ±0.1mm on arm length
TOL_ARM_WIDTH_MM: Final[float] = 0.05         # ±0.05mm on arm width
TOL_ARM_THICKNESS_MM: Final[float] = 0.05     # ±0.05mm on arm thickness
TOL_PIVOT_HOLE_MM: Final[float] = 0.02        # M5 clearance hole tolerance
TOL_ARC_MARK_POSITION_MM: Final[float] = 0.1  # ±0.1mm on etch position
TOL_ANGLE_SCALE_DEG: Final[float] = 0.5       # ±0.5° angle readout accuracy
TOL_EDGE_RADIUS_MM: Final[float] = 0.1        # ±0.1mm on edge deburr
TOL_FLATNESS_MM: Final[float] = 0.05          # Arm flatness over full length
TOL_LINEAR_MM: Final[float] = 0.1             # General linear dimensions
