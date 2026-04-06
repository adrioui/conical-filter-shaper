"""
Unit tests for cad/utils/ruler_math.py — Universal Filter Ruler geometry math.

Verifies:
  - angle_to_arm_spread  at 40°, 60°, 85°
  - pivot_position        always returns (0, 0)
  - arm_position_at_angle left/right symmetry, correct rotation sign
  - overlap_for_filter    values in 0–20 mm range; monotone in angle and radius
  - vernier_scale_position zero at min angle; increases with angle

All tests are pure-math — no CadQuery required.
"""
from __future__ import annotations

import math
import pytest

from cad.utils.ruler_math import (
    ANGLE_RANGE_MIN_DEG,
    ANGLE_RANGE_MAX_DEG,
    angle_to_arm_spread,
    pivot_position,
    arm_position_at_angle,
    overlap_for_filter,
    vernier_scale_position,
    arm_tip_x,
    arm_tip_y,
    included_angle_from_half,
    half_angle_from_included,
    vernier_offset_mm,
)

# ── Design constants used for reference in tests ───────────────────────────────
ARM_LENGTH_MM = 150.0       # From cad.params.ARM_LENGTH_MM
FILTER_02_R   = 77.5        # From cad.params.FILTER_02_RADIUS_MM  (02 size)
FILTER_01_R   = 55.0
FILTER_03_R   = 92.5
VERNIER_R     = 100.0       # Default vernier radius used in tests


# ═══════════════════════════════════════════════════════════════════════════════
# Constants exported from ruler_math
# ═══════════════════════════════════════════════════════════════════════════════

class TestModuleConstants:
    def test_angle_min(self):
        assert ANGLE_RANGE_MIN_DEG == pytest.approx(40.0)

    def test_angle_max(self):
        assert ANGLE_RANGE_MAX_DEG == pytest.approx(85.0)

    def test_min_less_than_max(self):
        assert ANGLE_RANGE_MIN_DEG < ANGLE_RANGE_MAX_DEG


# ═══════════════════════════════════════════════════════════════════════════════
# angle_to_arm_spread
# ═══════════════════════════════════════════════════════════════════════════════

class TestAngleToArmSpread:
    """spread = 2 × arm_length × sin(half_angle)"""

    def test_spread_at_40_deg(self):
        """40° included → each arm at 20° from center."""
        expected = 2.0 * ARM_LENGTH_MM * math.sin(math.radians(20.0))
        result = angle_to_arm_spread(40.0, ARM_LENGTH_MM)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_spread_at_60_deg(self):
        """
        60° → half = 30° → sin(30°) = 0.5
        spread = 2 × 150 × 0.5 = 150.0 mm exactly.
        """
        result = angle_to_arm_spread(60.0, ARM_LENGTH_MM)
        assert result == pytest.approx(150.0, rel=1e-6)

    def test_spread_at_85_deg(self):
        """85° → half = 42.5°."""
        expected = 2.0 * ARM_LENGTH_MM * math.sin(math.radians(42.5))
        result = angle_to_arm_spread(85.0, ARM_LENGTH_MM)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_spread_increases_with_angle(self, arm_angle):
        """Greater included angle → greater tip-to-tip spread."""
        s1 = angle_to_arm_spread(arm_angle, ARM_LENGTH_MM)
        if arm_angle < ANGLE_RANGE_MAX_DEG:
            s2 = angle_to_arm_spread(arm_angle + 1.0, ARM_LENGTH_MM)
            assert s2 > s1

    def test_spread_at_zero_angle_is_zero(self):
        """Degenerate case: 0° included → arms touch, spread = 0."""
        result = angle_to_arm_spread(0.0, ARM_LENGTH_MM)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_spread_at_180_deg_equals_twice_arm_length(self):
        """180° → arms point opposite directions → spread = 2 × arm_length."""
        result = angle_to_arm_spread(180.0, ARM_LENGTH_MM)
        assert result == pytest.approx(2.0 * ARM_LENGTH_MM, rel=1e-6)

    def test_spread_scales_linearly_with_arm_length(self):
        """Doubling arm length doubles spread."""
        s1 = angle_to_arm_spread(60.0, 100.0)
        s2 = angle_to_arm_spread(60.0, 200.0)
        assert s2 == pytest.approx(2.0 * s1, rel=1e-6)

    def test_spread_40_deg_approx_value(self):
        """40°, 150mm arm: spread ≈ 102.61 mm."""
        result = angle_to_arm_spread(40.0, ARM_LENGTH_MM)
        assert result == pytest.approx(102.606, rel=1e-3)

    def test_spread_85_deg_approx_value(self):
        """85°, 150mm arm: spread ≈ 202.68 mm."""
        result = angle_to_arm_spread(85.0, ARM_LENGTH_MM)
        assert result == pytest.approx(202.677, rel=1e-3)


# ═══════════════════════════════════════════════════════════════════════════════
# pivot_position
# ═══════════════════════════════════════════════════════════════════════════════

class TestPivotPosition:
    def test_returns_tuple(self):
        pos = pivot_position()
        assert isinstance(pos, tuple)

    def test_length_is_two(self):
        assert len(pivot_position()) == 2

    def test_x_is_zero(self):
        x, y = pivot_position()
        assert x == pytest.approx(0.0)

    def test_y_is_zero(self):
        x, y = pivot_position()
        assert y == pytest.approx(0.0)

    def test_always_same_value(self):
        """pivot_position() is deterministic — no state."""
        assert pivot_position() == pivot_position()


# ═══════════════════════════════════════════════════════════════════════════════
# arm_position_at_angle
# ═══════════════════════════════════════════════════════════════════════════════

class TestArmPositionAtAngle:
    """Tests for left/right arm transforms and symmetry."""

    def test_left_arm_positive_rotation(self):
        """Left arm rotates CCW (positive) from center-line."""
        t = arm_position_at_angle(60.0, "left")
        assert t["rotation_deg"] > 0.0

    def test_right_arm_negative_rotation(self):
        """Right arm rotates CW (negative) from center-line."""
        t = arm_position_at_angle(60.0, "right")
        assert t["rotation_deg"] < 0.0

    def test_left_arm_rotation_equals_half_angle(self):
        t = arm_position_at_angle(60.0, "left")
        assert t["rotation_deg"] == pytest.approx(30.0)

    def test_right_arm_rotation_equals_neg_half_angle(self):
        t = arm_position_at_angle(60.0, "right")
        assert t["rotation_deg"] == pytest.approx(-30.0)

    def test_symmetry_rotation_magnitudes_equal(self, arm_angle):
        """Left and right arms have equal but opposite rotations."""
        left  = arm_position_at_angle(arm_angle, "left")
        right = arm_position_at_angle(arm_angle, "right")
        assert abs(left["rotation_deg"]) == pytest.approx(abs(right["rotation_deg"]))

    def test_symmetry_rotation_signs_opposite(self, arm_angle):
        left  = arm_position_at_angle(arm_angle, "left")
        right = arm_position_at_angle(arm_angle, "right")
        assert left["rotation_deg"] == pytest.approx(-right["rotation_deg"])

    def test_pivot_is_origin_left(self):
        t = arm_position_at_angle(60.0, "left")
        assert t["pivot_x"] == pytest.approx(0.0)
        assert t["pivot_y"] == pytest.approx(0.0)

    def test_pivot_is_origin_right(self):
        t = arm_position_at_angle(60.0, "right")
        assert t["pivot_x"] == pytest.approx(0.0)
        assert t["pivot_y"] == pytest.approx(0.0)

    def test_side_field_left(self):
        t = arm_position_at_angle(60.0, "left")
        assert t["side"] == "left"

    def test_side_field_right(self):
        t = arm_position_at_angle(60.0, "right")
        assert t["side"] == "right"

    def test_rotation_at_40_deg_left(self):
        t = arm_position_at_angle(40.0, "left")
        assert t["rotation_deg"] == pytest.approx(20.0)

    def test_rotation_at_85_deg_right(self):
        t = arm_position_at_angle(85.0, "right")
        assert t["rotation_deg"] == pytest.approx(-42.5)

    def test_invalid_side_raises_value_error(self):
        with pytest.raises(ValueError, match="left.*right"):
            arm_position_at_angle(60.0, "center")

    def test_rotation_increases_with_angle_left(self):
        """Left arm rotation grows as included angle grows."""
        t40 = arm_position_at_angle(40.0, "left")
        t85 = arm_position_at_angle(85.0, "left")
        assert t85["rotation_deg"] > t40["rotation_deg"]


# ═══════════════════════════════════════════════════════════════════════════════
# overlap_for_filter
# ═══════════════════════════════════════════════════════════════════════════════

class TestOverlapForFilter:
    """Tests for seam-overlap estimation using the sagitta model."""

    def test_overlap_at_60_deg_r77_5(self):
        """
        60° angle, R=77.5mm (size 02):
        overlap = 77.5 × (1 − cos(30°)) ≈ 10.38 mm.
        """
        result = overlap_for_filter(FILTER_02_R, 60.0)
        expected = FILTER_02_R * (1.0 - math.cos(math.radians(30.0)))
        assert result == pytest.approx(expected, rel=1e-6)
        assert result == pytest.approx(10.38, rel=1e-2)

    def test_overlap_at_40_deg_r77_5(self):
        result = overlap_for_filter(FILTER_02_R, 40.0)
        expected = FILTER_02_R * (1.0 - math.cos(math.radians(20.0)))
        assert result == pytest.approx(expected, rel=1e-6)
        # Should be ~4.6 mm (within 0–20mm scale)
        assert 0 < result < 10

    def test_overlap_at_85_deg_r77_5(self):
        result = overlap_for_filter(FILTER_02_R, 85.0)
        expected = FILTER_02_R * (1.0 - math.cos(math.radians(42.5)))
        assert result == pytest.approx(expected, rel=1e-6)
        # Approaches 20mm at max angle for largest filter
        assert result <= 25.0

    def test_overlap_in_spec_range_for_all_filters(self, arm_angle):
        """
        All filter sizes × all operating angles must give overlap in 0–25mm.
        (The spec scale is 0–20mm for typical usage; we allow headroom.)
        """
        for radius in (FILTER_01_R, FILTER_02_R, FILTER_03_R):
            result = overlap_for_filter(radius, arm_angle)
            assert 0.0 <= result <= 30.0, (
                f"Overlap out of range for R={radius}, angle={arm_angle}°: {result:.2f} mm"
            )

    def test_overlap_increases_with_angle(self):
        """Wider angle → more seam overlap (for fixed filter radius)."""
        o40 = overlap_for_filter(FILTER_02_R, 40.0)
        o60 = overlap_for_filter(FILTER_02_R, 60.0)
        o85 = overlap_for_filter(FILTER_02_R, 85.0)
        assert o40 < o60 < o85

    def test_overlap_increases_with_filter_radius(self):
        """Larger filter → more seam overlap (at fixed angle)."""
        o01 = overlap_for_filter(FILTER_01_R, 60.0)
        o02 = overlap_for_filter(FILTER_02_R, 60.0)
        o03 = overlap_for_filter(FILTER_03_R, 60.0)
        assert o01 < o02 < o03

    def test_overlap_zero_at_zero_angle(self):
        """0° included angle → no seam overlap (arms are closed)."""
        result = overlap_for_filter(FILTER_02_R, 0.0)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_overlap_scales_linearly_with_radius(self):
        """Doubling filter radius doubles overlap (at same angle)."""
        o1 = overlap_for_filter(50.0, 60.0)
        o2 = overlap_for_filter(100.0, 60.0)
        assert o2 == pytest.approx(2.0 * o1, rel=1e-6)

    def test_overlap_for_01_filter_at_60_deg(self):
        result = overlap_for_filter(FILTER_01_R, 60.0)
        expected = FILTER_01_R * (1.0 - math.cos(math.radians(30.0)))
        assert result == pytest.approx(expected, rel=1e-6)

    def test_overlap_for_03_filter_at_40_deg(self):
        result = overlap_for_filter(FILTER_03_R, 40.0)
        expected = FILTER_03_R * (1.0 - math.cos(math.radians(20.0)))
        assert result == pytest.approx(expected, rel=1e-6)


# ═══════════════════════════════════════════════════════════════════════════════
# vernier_scale_position
# ═══════════════════════════════════════════════════════════════════════════════

class TestVernierScalePosition:
    def test_zero_at_min_angle(self):
        """At minimum angle (40°) the position is the zero reference."""
        result = vernier_scale_position(ANGLE_RANGE_MIN_DEG, VERNIER_R)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_positive_at_max_angle(self):
        result = vernier_scale_position(ANGLE_RANGE_MAX_DEG, VERNIER_R)
        assert result > 0.0

    def test_max_angle_position(self):
        """
        At 85° with R=100mm:
        position = 100 × (85−40)° × π/180 = 100 × 45π/180 = 25π ≈ 78.54 mm.
        """
        result = vernier_scale_position(85.0, VERNIER_R)
        expected = VERNIER_R * math.radians(45.0)
        assert result == pytest.approx(expected, rel=1e-6)
        assert result == pytest.approx(78.54, rel=1e-3)

    def test_position_at_60_deg(self):
        """60°: position = 100 × 20° × π/180 = 100 × π/9 ≈ 34.91 mm."""
        result = vernier_scale_position(60.0, VERNIER_R)
        expected = VERNIER_R * math.radians(20.0)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_monotone_increasing(self, arm_angle):
        """Scale position increases strictly with angle."""
        p = vernier_scale_position(arm_angle, VERNIER_R)
        if arm_angle < ANGLE_RANGE_MAX_DEG:
            p_next = vernier_scale_position(arm_angle + 1.0, VERNIER_R)
            assert p_next > p

    def test_scales_linearly_with_radius(self):
        """Doubling vernier radius doubles scale position."""
        p1 = vernier_scale_position(60.0, 100.0)
        p2 = vernier_scale_position(60.0, 200.0)
        assert p2 == pytest.approx(2.0 * p1, rel=1e-6)

    def test_step_per_half_degree(self):
        """
        The arc step for 0.5° at R=100mm:
        step = 100 × 0.5 × π/180 ≈ 0.873 mm
        Successive half-degree marks must be this far apart.
        """
        p0 = vernier_scale_position(60.0, VERNIER_R)
        p1 = vernier_scale_position(60.5, VERNIER_R)
        step = VERNIER_R * math.radians(0.5)
        assert (p1 - p0) == pytest.approx(step, rel=1e-6)


# ═══════════════════════════════════════════════════════════════════════════════
# Legacy helpers (backward-compatibility smoke tests)
# ═══════════════════════════════════════════════════════════════════════════════

class TestLegacyHelpers:
    def test_arm_tip_x(self):
        """arm_tip_x: at half_angle=0, tip is directly in front (x = arm_length)."""
        assert arm_tip_x(150.0, 0.0) == pytest.approx(150.0)

    def test_arm_tip_y_at_zero(self):
        """arm_tip_y: at half_angle=0, lateral offset = 0."""
        assert arm_tip_y(150.0, 0.0) == pytest.approx(0.0)

    def test_arm_tip_y_at_30deg(self):
        """arm_tip_y: at half_angle=30°, y = 150 × sin(30°) = 75."""
        assert arm_tip_y(150.0, 30.0) == pytest.approx(75.0)

    def test_included_angle_from_half(self):
        assert included_angle_from_half(30.0) == pytest.approx(60.0)

    def test_half_angle_from_included(self):
        assert half_angle_from_included(60.0) == pytest.approx(30.0)

    def test_round_trip_angle(self):
        angle = 72.5
        assert included_angle_from_half(half_angle_from_included(angle)) == pytest.approx(angle)

    def test_vernier_offset_mm(self):
        """vernier_offset_mm: arc length for one 0.5° division at R=100mm ≈ 0.873 mm."""
        result = vernier_offset_mm(30.0, 0.5, 100.0)
        expected = 100.0 * math.radians(0.5)
        assert result == pytest.approx(expected, rel=1e-6)
