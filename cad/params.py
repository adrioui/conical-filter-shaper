"""
Universal Conical Filter Shaper — Design Parameters
====================================================
Single source of truth for ALL dimensions, tolerances, and material specs.

Rules
-----
- All lengths in mm unless the name ends with a different unit suffix.
- All angles in degrees; full included angle unless named *_half_angle*.
- Every constant in this file is referenced at least once in cad/components/ or tests/.
- Do NOT hardcode numbers in component files — always import from here.

Revision: 0.1  (bump via scripts/bump_revision.py)
Spec reference: docs/design_spec.md
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Final

# ── Revision ──────────────────────────────────────────────────────────────────
REVISION: Final[str] = "0.1"

# ── Input paper target ────────────────────────────────────────────────────────
# V1 workflow assumes standard pre-seamed conical paper filters, not flat circular blanks.
REFERENCE_PAPER_FAMILY: Final[str] = "Common 02-class pre-seamed cone papers"
PAPER_ABOVE_BASE_RIM_MM: Final[float] = 10.0  # Nominal paper above shell base at any preset


# ═══════════════════════════════════════════════════════════════════════════════
# CONE PRESETS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ConePreset:
    """
    Geometric definition of one angle preset.
    All dimensions derive from `slant_height_mm` and `half_angle_deg`.
    Verify with: tests/test_params.py::test_base_radius_within_tolerance
    """
    label: str
    included_angle_deg: float       # Full apex angle (side-to-side)
    half_angle_deg: float           # = included_angle / 2
    slant_height_mm: float          # Generating-line length (apex → base edge)
    base_radius_mm: float           # r = slant * sin(half_angle) — rounded to 0.1 mm
    axial_height_mm: float          # h = slant * cos(half_angle) — rounded to 0.1 mm
    cam_dwell_radius_mm: float      # Shell base-pin radius in cam track at this preset
    target_drippers: list[str] = field(default_factory=list)

PRESET_1 = ConePreset(
    label="P1",
    included_angle_deg=48.0,
    half_angle_deg=24.0,
    slant_height_mm=82.0,
    base_radius_mm=33.3,    # 82 × sin(24°) = 33.31
    axial_height_mm=74.9,   # 82 × cos(24°) = 74.91
    cam_dwell_radius_mm=33.3,
    target_drippers=["Timemore B75", "Origami Narrow"],
)

PRESET_2 = ConePreset(
    label="P2",
    included_angle_deg=60.0,
    half_angle_deg=30.0,
    slant_height_mm=82.0,
    base_radius_mm=41.0,    # 82 × sin(30°) = 41.00
    axial_height_mm=71.0,   # 82 × cos(30°) = 71.01
    cam_dwell_radius_mm=41.0,
    target_drippers=["Hario V60 #2", "April Brewer", "Cafec Flower"],
)

PRESET_3 = ConePreset(
    label="P3",
    included_angle_deg=80.0,
    half_angle_deg=40.0,
    slant_height_mm=82.0,
    base_radius_mm=52.7,    # 82 × sin(40°) = 52.71
    axial_height_mm=62.8,   # 82 × cos(40°) = 62.82
    cam_dwell_radius_mm=52.7,
    target_drippers=["UFO Dripper", "Origami Wide"],
)

PRESETS: Final[list[ConePreset]] = [PRESET_1, PRESET_2, PRESET_3]
DEFAULT_PRESET: Final[ConePreset] = PRESET_2


# ═══════════════════════════════════════════════════════════════════════════════
# SHELL HALF GEOMETRY  (parts: shell_half_l, shell_half_r)
# ═══════════════════════════════════════════════════════════════════════════════

# Wall thickness
SHELL_WALL_THICKNESS_MM: Final[float] = 2.5       # Minimum; see §3.1 of spec
SHELL_BASE_TAB_THICKNESS_MM: Final[float] = 4.0   # Thicker at cam follower boss
SHELL_BASE_TAB_EXTENSION_MM: Final[float] = 12.0  # Extension below cone base

# Surface finish callout (used in drawing annotations)
SHELL_FILTER_FACE_RA_UM: Final[float] = 0.8       # Ra ≤ 0.8 µm on filter contact face

# Seam relief — prevents filter paper snagging at split line
SHELL_SEAM_RELIEF_CHAMFER_MM: Final[float] = 0.2

# Cam follower pin press-fit hole in base tab
SHELL_FOLLOWER_BOSS_OD_MM: Final[float] = 10.0    # Boss OD around follower bore
SHELL_FOLLOWER_BORE_DIA_MM: Final[float] = 4.0    # M4 shoulder bolt shank

# Material (for BOM generation)
SHELL_MATERIAL: Final[str] = "POM-C (Acetal Copolymer) — food-grade"
SHELL_PROCESS: Final[str] = "CNC milled"


# ═══════════════════════════════════════════════════════════════════════════════
# TIP INSERT BLOCK  (part: tip_insert_block)
# ═══════════════════════════════════════════════════════════════════════════════

TIP_BLOCK_WIDTH_MM: Final[float] = 18.0
TIP_BLOCK_DEPTH_MM: Final[float] = 18.0
TIP_BLOCK_HEIGHT_MM: Final[float] = 22.0
TIP_EXTERNAL_EDGE_FILLET_MM: Final[float] = 0.5

# Tip locator dimple (receives the closed apex of a pre-seamed paper cone)
TIP_DIMPLE_DIAMETER_MM: Final[float] = 3.0
TIP_DIMPLE_DEPTH_MM: Final[float] = 2.0
TIP_DIMPLE_INCLUDED_ANGLE_DEG: Final[float] = 60.0
TIP_DIMPLE_EDGE_FILLET_MM: Final[float] = 0.5

# Hinge pin bore
TIP_HINGE_BORE_DIA_MM: Final[float] = 3.0  # M3 shoulder bolt clearance
TIP_HINGE_BORE_AXIS: Final[str] = "transverse"  # perpendicular to cone axis
TIP_HINGE_BORE_Z_MM: Final[float] = 5.0  # Bore axis height above dimple-face datum

# Ejection spring chamber / axial bore stack
# Current honest V1 CAD models the 4.0 mm chamber as top-entry blind geometry so the
# tip dimple remains intact; the final tip breakout / guide-land detail is still pending.
TIP_EJECTION_BORE_DIA_MM: Final[float] = 4.0
TIP_EJECTION_CHAMBER_DEPTH_MM: Final[float] = 15.0
EJECTION_GUIDE_BORE_DIA_MM: Final[float] = 3.0

# Surface finish
TIP_FACE_RA_UM: Final[float] = 0.4  # Ra ≤ 0.4 µm; electropolished after machining

TIP_MATERIAL: Final[str] = "SS 316L — CNC turned + milled, electropolished"
TIP_PROCESS: Final[str] = "CNC turned + milled"


# ═══════════════════════════════════════════════════════════════════════════════
# ANGLE-SET RING / CAM RING  (part: cam_ring)
# ═══════════════════════════════════════════════════════════════════════════════

CAM_RING_OD_MM: Final[float] = 120.0
CAM_RING_BORE_MM: Final[float] = 60.0   # Bore clears ejection rod, housing features, and assembly tooling; shells sit above the ring.
CAM_RING_THICKNESS_MM: Final[float] = 14.0

# Cam track (dual-spiral, open-face)
CAM_TRACK_WIDTH_MM: Final[float] = 5.0   # Clears M4 follower pin Ø 3.9 mm
CAM_TRACK_DEPTH_MM: Final[float] = 4.0
CAM_DWELL_ARC_DEG: Final[float] = 12.0   # Dwell at each preset
CAM_TRANSITION_ARC_DEG: Final[float] = 48.0  # Sinusoidal ramp between presets
CAM_TRACK_RA_UM: Final[float] = 1.6

# Follower pin
CAM_FOLLOWER_PIN_DIA_MM: Final[float] = 4.0   # M4 SS 316L shoulder bolt
CAM_FOLLOWER_SHOULDER_LENGTH_MM: Final[float] = 5.0  # Engages cam track floor

# Ring rotation per click
CAM_RING_CLICK_DEG: Final[float] = 60.0   # 3 presets × 60° = 180° half-turn
CAM_SYMMETRY_FOLD: Final[int] = 6         # 6-fold alternating (2 followers × 3 presets)

CAM_RING_MATERIAL: Final[str] = "6061-T6 Aluminium — Type II anodized, hard-black"
CAM_RING_PROCESS: Final[str] = "CNC milled + Type II anodize"


# ═══════════════════════════════════════════════════════════════════════════════
# HANDLE HOUSING  (part: handle_housing)
# ═══════════════════════════════════════════════════════════════════════════════

HANDLE_OD_MM: Final[float] = 42.0         # Ergonomic grip diameter
HANDLE_LENGTH_MM: Final[float] = 65.0
GRIP_INSERT_WALL_MM: Final[float] = 3.0
HOUSING_RING_BORE_MM: Final[float] = 120.2   # CAM_RING_OD + 0.2 mm diametral clearance
HOUSING_FLANGE_OD_MM: Final[float] = 132.0
HOUSING_FLANGE_HEIGHT_MM: Final[float] = 18.0
HOUSING_TRANSITION_CHAMFER_MM: Final[float] = 5.0
HOUSING_RING_BORE_FLOOR_MM: Final[float] = 3.0

# Detent pocket (tangential blind bore into ring bore wall)
DETENT_POCKET_DIA_MM: Final[float] = 4.1   # Ball + ~0.1 mm clearance
DETENT_POCKET_DEPTH_MM: Final[float] = 9.0  # Spring FL + ball + set screw

# Angle indicator window (laser-etched labels visible through slot)
ANGLE_WINDOW_WIDTH_MM: Final[float] = 8.0
ANGLE_WINDOW_HEIGHT_MM: Final[float] = 6.0

BASE_CAP_THICKNESS_MM: Final[float] = 5.0
BASE_CAP_OD_MM: Final[float] = 130.0
BASE_CAP_SNAP_DEPTH_MM: Final[float] = 2.0
BASE_CAP_SNAP_LIP_MM: Final[float] = 1.5

HOUSING_MATERIAL: Final[str] = "6061-T6 Aluminium — CNC turned + milled + Type II anodize"
HOUSING_PROCESS: Final[str] = "CNC turned + milled"


# ═══════════════════════════════════════════════════════════════════════════════
# DETENT ASSEMBLY  (hardware — not a machined part file)
# ═══════════════════════════════════════════════════════════════════════════════

DETENT_BALL_DIAMETER_MM: Final[float] = 4.0       # SS 316L grade G25
DETENT_SPRING_FREE_LENGTH_MM: Final[float] = 10.0
DETENT_SPRING_INSTALLED_LENGTH_MM: Final[float] = 7.0   # 3 mm compression
DETENT_SPRING_PRELOAD_N: Final[float] = 3.2               # Approx at installation
DETENT_DIMPLE_DEPTH_MM: Final[float] = 1.4         # ~35% of ball diameter (critical)
DETENT_DIMPLE_RADIUS_MM: Final[float] = 2.2         # 110% of ball radius
DETENT_POSITIONS: Final[int] = 3
DETENT_SPACING_DEG: Final[float] = 60.0

# Ring rim surface finish at detent dimple zone
DETENT_RIM_RA_UM: Final[float] = 0.8
# IMPORTANT: mask detent dimples before anodize — see manufacturing/surface_finish_notes.md


# ═══════════════════════════════════════════════════════════════════════════════
# SEAM GUIDE FIN  (part file remains overlap_fin.py for now)
# ═══════════════════════════════════════════════════════════════════════════════

FIN_THICKNESS_MM: Final[float] = 0.5       # SS 301 half-hard spring steel
FIN_WIDTH_MM: Final[float] = 6.0
FIN_LENGTH_MM: Final[float] = 75.0

# Fin slot in Shell R
FIN_SLOT_WIDTH_MM: Final[float] = 0.55     # +0.05 / -0.00 tolerance
FIN_SLOT_DEPTH_MM: Final[float] = 7.0
FIN_SLOT_LENGTH_MM: Final[float] = 76.0   # Slightly longer than fin for insertion

# Serration retention
FIN_SERRATION_PITCH_MM: Final[float] = 0.5
FIN_SERRATION_HEIGHT_MM: Final[float] = 0.2
FIN_PULLOUT_FORCE_N: Final[float] = 10.0  # Nominal; range 8–12 N acceptable

# Guide reference positions for tuning factory seam bias/relief.
# Legacy overlap-oriented aliases are kept below until real geometry replaces the stubs.
FIN_GUIDE_POSITIONS_MM: Final[list[float]] = [5.0, 7.5, 10.0, 12.5, 15.0]
FIN_DEFAULT_GUIDE_POSITION_MM: Final[float] = 10.0
FIN_OVERLAP_POSITIONS_MM: Final[list[float]] = FIN_GUIDE_POSITIONS_MM
FIN_DEFAULT_OVERLAP_MM: Final[float] = FIN_DEFAULT_GUIDE_POSITION_MM

FIN_MATERIAL: Final[str] = "SS 301 half-hard spring steel — laser-cut + press-formed"
FIN_PROCESS: Final[str] = "Laser cut (do NOT anneal after cut)"


# ═══════════════════════════════════════════════════════════════════════════════
# EJECTION SYSTEM  (parts: ejection_rod, button cap)
# ═══════════════════════════════════════════════════════════════════════════════

EJECTION_ROD_DIAMETER_MM: Final[float] = 3.0   # h6 tolerance
EJECTION_ROD_LENGTH_MM: Final[float] = 100.0
EJECTION_ROD_RECESS_MM: Final[float] = 1.5    # Rod tip recessed below tip face at rest
EJECTION_STROKE_MM: Final[float] = 5.0         # Travel when button pressed
EJECTION_ROD_RA_UM: Final[float] = 0.4

EJECTION_BUTTON_DIAMETER_MM: Final[float] = 10.0
EJECTION_BUTTON_MATERIAL: Final[str] = "POM-C — CNC turned, knurled rim"

EJECTION_SPRING_FREE_LENGTH_MM: Final[float] = 15.0
EJECTION_SPRING_FORCE_REST_N: Final[float] = 1.5
EJECTION_SPRING_FORCE_EXTENDED_N: Final[float] = 2.8

EJECTION_ROD_MATERIAL: Final[str] = "SS 304 — CNC turned, h6 ground finish"
EJECTION_ROD_PROCESS: Final[str] = "CNC turned"


# ═══════════════════════════════════════════════════════════════════════════════
# HARDWARE (bought-in; for BOM only)
# ═══════════════════════════════════════════════════════════════════════════════

HINGE_PIN_SPEC: Final[str] = "M3 × 20 mm SS 316L shoulder bolt, DIN 6912, head flush"
FOLLOWER_PIN_SPEC: Final[str] = "M4 SS 316L shoulder bolt, 4 mm shoulder Ø × 5 mm"
DETENT_SETSCREW_SPEC: Final[str] = "M4 × 8 mm SS 316L grub screw DIN 913, Loctite 243"
PTFE_WASHER_THICKNESS_MM: Final[float] = 0.5
PTFE_WASHER_SPEC: Final[str] = "PTFE, 0.5 mm thick, ID to clear ring bore"
ASSEMBLY_SCREWS_SPEC: Final[str] = "M3 SHCS ISO 4762, SS 316L, qty 4"
THREAD_LOCKER: Final[str] = "Loctite 243 (medium-strength removable)"


# ═══════════════════════════════════════════════════════════════════════════════
# TOLERANCE GROUPS  (ISO 286 fit pairs; used in tests/test_tolerances.py)
# ═══════════════════════════════════════════════════════════════════════════════

# Each entry: (description, hole_spec, shaft_spec, clearance_range_mm or "interference")
TOLERANCE_GROUPS: Final[dict[str, tuple[str, str, str]]] = {
    # Group A — Angle-critical
    "cam_track_dwell_P1": ("Cam dwell radius P1", "±0.10 mm", "ø33.3 mm nominal", "±0.17° angle"),
    "cam_track_dwell_P2": ("Cam dwell radius P2", "±0.10 mm", "ø41.0 mm nominal", "±0.14° angle"),
    "cam_track_dwell_P3": ("Cam dwell radius P3", "±0.10 mm", "ø52.7 mm nominal", "±0.11° angle"),
    # Group B — Tip locator
    "tip_dimple_depth":   ("Tip dimple depth", "2.0 mm +0.15/-0.00", "", ""),
    # Group C — Overlap stop
    "fin_slot_width":     ("Fin slot width", "0.55 mm +0.05/-0.00", "0.50 mm ±0.02", "0.03–0.07 mm clearance"),
    # Group D — Rotary interfaces
    "ring_in_housing":    ("Ring OD / housing bore", "120.2 mm +0.0/+0.05", "120.0 mm -0.0/-0.05", "0.1–0.25 mm diametral"),
    # Group E — Ejection system (planned stepped-bore detail)
    "ejection_rod_bore":  ("Ejection rod guide land", "H7 (3.000–3.010)", "h6 (3.000–2.994)", "0.000–0.016 mm sliding"),
    # Press fits
    "follower_pin_press": ("Follower pin in POM boss", "H7 in POM", "n6 SS", "0.010–0.021 mm interference"),
    "hinge_pin_bore":     ("Hinge pin / shell bore", "H7", "f7", "0.010–0.030 mm clearance"),
}

ANGLE_ACCURACY_TARGET_DEG: Final[float] = 0.5   # ±0.5° included angle at each preset


# ═══════════════════════════════════════════════════════════════════════════════
# OVERALL TOOL ENVELOPE
# ═══════════════════════════════════════════════════════════════════════════════

TOOL_HEIGHT_AT_80DEG_MM: Final[float] = (
    PRESET_3.axial_height_mm     # cone
    + CAM_RING_THICKNESS_MM      # ring
    + HANDLE_LENGTH_MM           # handle
    + 5.0                        # base cap
)  # ≈ 146.8 mm using axial height; the older 166 mm reference card used slant-height shorthand.

TOOL_MAX_WIDTH_MM: Final[float] = PRESET_3.base_radius_mm * 2  # ≈ 105.4 mm
TOOL_MASS_ESTIMATE_G: Final[tuple[float, float]] = (145.0, 185.0)  # min, max
