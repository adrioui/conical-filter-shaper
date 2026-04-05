#!/usr/bin/env python3
"""
Validate geometry: tolerance stacks, clearance checks, cam track closure.
Runs without CadQuery (pure-math checks only).
For CQ interpenetration checks, CadQuery must be installed.

Usage:
    python scripts/validate_geometry.py
"""
from __future__ import annotations
import sys
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import cad.params as P
from cad.utils.cone_math import included_angle_from_radii, base_radius
from cad.utils.cam_geometry import build_cam_track

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

errors = []


def check(condition: bool, label: str, detail: str = "") -> None:
    status = PASS if condition else FAIL
    print(f"  {status}  {label}")
    if detail:
        print(f"       {detail}")
    if not condition:
        errors.append(label)


print("\n" + "─" * 60)
print("  Geometry Validation — conical-filter-shaper")
print(f"  Revision: {P.REVISION}")
print("─" * 60)

# ── 1. Cone angle accuracy ─────────────────────────────────────────────────────
print("\n[1] Cone angle back-calculation")
for preset in P.PRESETS:
    recovered = included_angle_from_radii(preset.base_radius_mm, preset.slant_height_mm)
    err = abs(recovered - preset.included_angle_deg)
    check(
        err <= P.ANGLE_ACCURACY_TARGET_DEG,
        f"{preset.label} ({preset.included_angle_deg}°): error = {err:.3f}°",
        f"    cam_dwell_r={preset.cam_dwell_radius_mm} mm, recovered={recovered:.3f}°",
    )

# ── 2. Cam track closure ───────────────────────────────────────────────────────
# The ring has 6-fold alternating symmetry: 2 followers × 3 presets.
# Each follower's track spans 180° (one half-rotation covers all 3 presets).
# The two followers are offset 180° apart, together filling the full 360°.
print("\n[2] Cam track arc closure (per follower = 180°)")
n = len(P.PRESETS)
total_arc_per_follower = n * (P.CAM_DWELL_ARC_DEG + P.CAM_TRANSITION_ARC_DEG)
check(
    abs(total_arc_per_follower - 180.0) < 0.01,
    f"Per-follower arc sum = {total_arc_per_follower}°  (must = 180° — 2 followers fill 360°)",
)

# ── 3. Cam track radial reach covers max preset ────────────────────────────────
# Shell base pins ride in cam track on the UPPER FACE of the ring, not through the bore.
# The ring bore (60 mm) just clears the handle internals (ejection rod, etc.).
# What matters: cam track's outermost dwell radius ≤ (CAM_RING_OD/2 − track_wall).
print("\n[3] Cam track radial reach vs ring OD")
max_dwell_r = max(p.cam_dwell_radius_mm for p in P.PRESETS)
# Minimum wall: 4.0 mm for 6061-T6 Al at these loads. P3 actual wall = 4.8 mm.
track_wall_mm = 4.0  # absolute minimum (design target is 4.8 mm at P3)
max_allowed_r = (P.CAM_RING_OD_MM / 2.0) - (P.CAM_TRACK_WIDTH_MM / 2.0) - track_wall_mm
track_outer = max_dwell_r + P.CAM_TRACK_WIDTH_MM / 2.0
actual_wall = P.CAM_RING_OD_MM / 2.0 - track_outer
check(
    max_dwell_r <= max_allowed_r,
    f"Max dwell radius {max_dwell_r} mm ≤ allowed {max_allowed_r:.1f} mm  "
    f"(actual wall at P3 = {actual_wall:.1f} mm, min = {track_wall_mm} mm)",
)

# ── 4. Detent dimple proportions ────────────────────────────────────────────────
# Convention used in this repo: detent dimple depth is compared against ball diameter.
# Example: 1.4 mm / 4.0 mm = 35%.
print("\n[4] Detent dimple geometry")
ball_r = P.DETENT_BALL_DIAMETER_MM / 2.0
ball_d = P.DETENT_BALL_DIAMETER_MM
ratio_of_diameter = P.DETENT_DIMPLE_DEPTH_MM / ball_d   # 1.4/4.0 = 35%
check(
    0.28 <= ratio_of_diameter <= 0.45,
    f"Dimple depth/diameter = {ratio_of_diameter:.2%} (target 28–45% of ball diameter; "
    f"1.4mm/{ball_d}mm = {ratio_of_diameter:.0%})",
)
check(
    P.DETENT_DIMPLE_RADIUS_MM > ball_r,
    f"Dimple radius {P.DETENT_DIMPLE_RADIUS_MM} mm > ball radius {ball_r} mm",
)

# ── 5. Ejection stroke clears tip recess ──────────────────────────────────────
print("\n[5] Ejection system")
check(
    P.EJECTION_STROKE_MM > P.EJECTION_ROD_RECESS_MM,
    f"Stroke {P.EJECTION_STROKE_MM} mm > recess {P.EJECTION_ROD_RECESS_MM} mm",
)

# ── 6. Fin slot clearance ──────────────────────────────────────────────────────
print("\n[6] Fin slot clearance")
fin_clearance = P.FIN_SLOT_WIDTH_MM - P.FIN_THICKNESS_MM
check(
    0.02 <= fin_clearance <= 0.10,
    f"Clearance = {fin_clearance:.3f} mm (target 0.020–0.100 mm)",
)

# ── 7. Tip-block internal clearance ───────────────────────────────────────────
print("\n[7] Tip-block blind chamber vs hinge bore")
chamber_bottom_z = P.TIP_BLOCK_HEIGHT_MM - P.TIP_EJECTION_CHAMBER_DEPTH_MM
hinge_top_z = P.TIP_HINGE_BORE_Z_MM + (P.TIP_HINGE_BORE_DIA_MM / 2.0)
chamber_clearance = chamber_bottom_z - hinge_top_z
check(
    chamber_clearance >= 0.5,
    f"Blind chamber / hinge clearance = {chamber_clearance:.3f} mm (min 0.5 mm)",
)

# ── 8. Tolerance stack — worst-case linear ────────────────────────────────────
print("\n[8] Worst-case angle tolerance stack (P1 48°)")
slant = P.PRESET_1.slant_height_mm
r = P.PRESET_1.base_radius_mm
half_rad = math.radians(P.PRESET_1.half_angle_deg)
dangle_dr = math.degrees(2.0 / math.sqrt(slant**2 - r**2))
cam_err   = 0.10 * dangle_dr
play_err  = 0.05 * dangle_dr
slant_err = 0.20 * math.degrees(math.sin(half_rad) / slant)
hinge_err = 0.02 * dangle_dr
total_err = cam_err + play_err + slant_err + hinge_err
check(
    total_err <= P.ANGLE_ACCURACY_TARGET_DEG,
    f"Linear stack = ±{total_err:.3f}°  (limit ±{P.ANGLE_ACCURACY_TARGET_DEG}°)",
    f"    cam={cam_err:.3f}°  play={play_err:.3f}°  slant={slant_err:.3f}°  hinge={hinge_err:.3f}°",
)

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
if errors:
    print(f"  {FAIL}  {len(errors)} check(s) FAILED:")
    for e in errors:
        print(f"     • {e}")
    sys.exit(1)
else:
    print(f"  {PASS}  All checks passed.")
print("─" * 60 + "\n")
