"""
Unit tests for cad/utils/ruler_math.py — Universal Coffee Filter Ruler v3.0 geometry.

Verifies:
  - cone_half_angle_to_sector conversion
  - sector_to_cone_half_angle inverse conversion
  - v_opening_width calculation
  - arm_tip_spread at various angles
  - stand_height at various angles
  - arc_mark_intersects_arm intersection check
  - validate_angle range validation

All tests are pure-math — no CadQuery required.
"""
from __future__ import annotations

import math
import pytest

from cad.utils.ruler_math import (
    ANGLE_RANGE_MIN_DEG,
    ANGLE_RANGE_MAX_DEG,
    DEFAULT_ARM_LENGTH_MM,
    cone_half_angle_to_sector,
    sector_to_cone_half_angle,
    v_opening_width,
    arm_tip_spread,
    stand_height,
    arc_mark_intersects_arm,
    validate_angle,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Module constants
# ═══════════════════════════════════════════════════════════════════════════════

class TestModuleConstants:
    def test_angle_min(self):
        assert ANGLE_RANGE_MIN_DEG == pytest.approx(40.0)

    def test_angle_max(self):
        assert ANGLE_RANGE_MAX_DEG == pytest.approx(85.0)

    def test_min_less_than_max(self):
        assert ANGLE_RANGE_MIN_DEG < ANGLE_RANGE_MAX_DEG

    def test_default_arm_length(self):
        assert DEFAULT_ARM_LENGTH_MM == pytest.approx(120.0)


# ═══════════════════════════════════════════════════════════════════════════════
# Cone half-angle to sector conversion
# ═══════════════════════════════════════════════════════════════════════════════

class TestConeHalfAngleToSector:
    """sector = 360 × sin(half_angle)"""

    def test_v60_cone_half_angle(self):
        """
        V60 filter: 60° cone → half_angle = 30°
        sector = 360 × sin(30°) = 360 × 0.5 = 180.0°
        """
        result = cone_half_angle_to_sector(30.0)
        assert result == pytest.approx(180.0, rel=1e-6)

    def test_sd1r_cone_half_angle(self):
        """
        SD1R: 48° cone → half_angle = 24°
        sector = 360 × sin(24°) ≈ 146.5°
        """
        result = cone_half_angle_to_sector(24.0)
        assert result == pytest.approx(146.5, rel=1e-2)

    def test_ufo_cone_half_angle(self):
        """
        UFO (Kalita Wave 155): 80° cone → half_angle = 40°
        sector = 360 × sin(40°) ≈ 231.4°
        """
        result = cone_half_angle_to_sector(40.0)
        assert result == pytest.approx(231.4, rel=1e-1)

    def test_sector_scales_with_half_angle(self):
        """Larger half-angle → larger sector."""
        s1 = cone_half_angle_to_sector(20.0)
        s2 = cone_half_angle_to_sector(30.0)
        assert s2 > s1


# ═══════════════════════════════════════════════════════════════════════════════
# Sector to cone half-angle (inverse conversion)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSectorToConeHalfAngle:
    """half_angle = arcsin(sector / 360)"""

    def test_inverse_of_v60(self):
        """Sector 180° → half_angle = 30°."""
        result = sector_to_cone_half_angle(180.0)
        assert result == pytest.approx(30.0, rel=1e-2)

    def test_inverse_round_trip(self):
        """Round-trip conversion should return close to original."""
        original = 35.0
        sector = cone_half_angle_to_sector(original)
        recovered = sector_to_cone_half_angle(sector)
        assert recovered == pytest.approx(original, rel=1e-3)


# ═════════════════════════════════════════════════════════════════════════────══
# V-opening width
# ═══════════════════════════════════════════════════════════════════════════════

class TestVOpeningWidth:
    """w = 2 × distance × sin(angle / 2)"""

    def test_v60_at_02_mark(self):
        """
        V60 at 60° at 116mm radius (V60-02)
        w = 2 × 116 × sin(30°) = 232 × 0.5 = 116.0 mm
        """
        result = v_opening_width(116.0, 60.0)
        assert result == pytest.approx(116.0, rel=1e-6)

    def test_width_at_60_deg_full_arm(self):
        """At 60° at arm length 120mm: w = 2 × 120 × 0.5 = 120.0 mm."""
        result = v_opening_width(120.0, 60.0)
        assert result == pytest.approx(120.0, rel=1e-6)

    def test_width_at_40_deg(self):
        """40° → half = 20° → sin(20°) ≈ 0.342."""
        expected = 2.0 * 120.0 * math.sin(math.radians(20.0))
        result = v_opening_width(120.0, 40.0)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_width_at_85_deg(self):
        """85° → half = 42.5°."""
        expected = 2.0 * 120.0 * math.sin(math.radians(42.5))
        result = v_opening_width(120.0, 85.0)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_width_increases_with_angle(self, ruler_angle):
        """Greater angle → greater V-opening width."""
        w1 = v_opening_width(100.0, ruler_angle)
        if ruler_angle < ANGLE_RANGE_MAX_DEG:
            w2 = v_opening_width(100.0, ruler_angle + 1.0)
            assert w2 > w1

    def test_width_increases_with_distance(self):
        """Greater distance from pivot → greater V-opening width."""
        w1 = v_opening_width(50.0, 60.0)
        w2 = v_opening_width(100.0, 60.0)
        assert w2 > w1

    def test_width_at_zero_angle_is_zero(self):
        """0° included → arms touch → width = 0."""
        result = v_opening_width(120.0, 0.0)
        assert result == pytest.approx(0.0, abs=1e-10)


# ═══════════════════════════════════════════════════════════════════════════════
# Arm tip spread
# ═══════════════════════════════════════════════════════════════════════════════

class TestArmTipSpread:
    """spread = 2 × arm_length × sin(angle / 2)"""

    def test_spread_at_60_deg(self):
        """60° → spread = 2 × 120 × 0.5 = 120.0 mm."""
        result = arm_tip_spread(60.0, DEFAULT_ARM_LENGTH_MM)
        assert result == pytest.approx(120.0, rel=1e-6)

    def test_spread_at_40_deg(self):
        """40° → half = 20° → spread ≈ 82.82 mm."""
        result = arm_tip_spread(40.0, DEFAULT_ARM_LENGTH_MM)
        assert result == pytest.approx(82.82, rel=1e-2)

    def test_spread_at_85_deg(self):
        """85° → half = 42.5°."""
        result = arm_tip_spread(85.0, DEFAULT_ARM_LENGTH_MM)
        expected = 2.0 * DEFAULT_ARM_LENGTH_MM * math.sin(math.radians(42.5))
        assert result == pytest.approx(expected, rel=1e-6)

    def test_spread_increases_with_angle(self, ruler_angle):
        """Greater angle → greater tip spread."""
        s1 = arm_tip_spread(ruler_angle, DEFAULT_ARM_LENGTH_MM)
        if ruler_angle < ANGLE_RANGE_MAX_DEG:
            s2 = arm_tip_spread(ruler_angle + 1.0, DEFAULT_ARM_LENGTH_MM)
            assert s2 > s1

    def test_spread_scales_linearly_with_arm_length(self):
        """Doubling arm length doubles spread."""
        s1 = arm_tip_spread(60.0, 100.0)
        s2 = arm_tip_spread(60.0, 200.0)
        assert s2 == pytest.approx(2.0 * s1, rel=1e-6)


# ═══════════════════════════════════════════════════════════════════════════════
# Stand height
# ═══════════════════════════════════════════════════════════════════════════════

class TestStandHeight:
    """height = arm_length × cos(angle / 2)"""

    def test_height_at_60_deg(self):
        """60° → half = 30° → cos(30°) ≈ 0.866 → h ≈ 103.92 mm."""
        result = stand_height(60.0, DEFAULT_ARM_LENGTH_MM)
        assert result == pytest.approx(103.92, rel=1e-2)

    def test_height_at_40_deg(self):
        """40° → half = 20° → cos(20°) ≈ 0.9397 → h ≈ 112.76 mm."""
        result = stand_height(40.0, DEFAULT_ARM_LENGTH_MM)
        assert result == pytest.approx(112.76, rel=1e-2)

    def test_height_at_85_deg(self):
        """85° → half = 42.5°."""
        result = stand_height(85.0, DEFAULT_ARM_LENGTH_MM)
        expected = DEFAULT_ARM_LENGTH_MM * math.cos(math.radians(42.5))
        assert result == pytest.approx(expected, rel=1e-6)

    def test_height_decreases_with_angle(self):
        """Wider angle → shorter stand height."""
        h40 = stand_height(40.0, DEFAULT_ARM_LENGTH_MM)
        h60 = stand_height(60.0, DEFAULT_ARM_LENGTH_MM)
        h85 = stand_height(85.0, DEFAULT_ARM_LENGTH_MM)
        assert h40 > h60 > h85

    def test_height_at_zero_deg(self):
        """0° → arms together → height = full arm length."""
        result = stand_height(0.0, DEFAULT_ARM_LENGTH_MM)
        assert result == pytest.approx(DEFAULT_ARM_LENGTH_MM, rel=1e-6)

    def test_height_at_180_deg_is_zero(self):
        """180° → arms flat → height = 0."""
        result = stand_height(180.0, DEFAULT_ARM_LENGTH_MM)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_height_scales_linearly_with_arm_length(self):
        """Doubling arm length doubles height."""
        h1 = stand_height(60.0, 100.0)
        h2 = stand_height(60.0, 200.0)
        assert h2 == pytest.approx(2.0 * h1, rel=1e-6)

    def test_height_positive_in_operating_range(self, ruler_angle):
        """All operating angles give positive stand height."""
        h = stand_height(ruler_angle, DEFAULT_ARM_LENGTH_MM)
        assert h > 0


# ═══════════════════════════════════════════════════════════════════════════════
# Arc mark intersection check
# ═══════════════════════════════════════════════════════════════════════════════

class TestArcMarkIntersectsArm:
    """Check if an arc mark at given radius intersects the tapered arm."""

    def test_arc_01_within_arm(self):
        """Arc 01 at 95mm radius is within 120mm arm → should intersect."""
        result = arc_mark_intersects_arm(
            arc_radius=95.0,
            arm_length=120.0,
            arm_width_narrow=25.0,
            arm_width_wide=65.0,
        )
        assert result is True

    def test_arc_at_end_of_arm(self):
        """Arc exactly at end of arm (radius = arm_length) - should not intersect."""
        result = arc_mark_intersects_arm(
            arc_radius=120.0,
            arm_length=120.0,
            arm_width_narrow=25.0,
            arm_width_wide=65.0,
        )
        assert result is False

    def test_arc_beyond_arm(self):
        """Arc beyond arm length (radius > arm_length) - should not intersect."""
        result = arc_mark_intersects_arm(
            arc_radius=150.0,
            arm_length=120.0,
            arm_width_narrow=25.0,
            arm_width_wide=65.0,
        )
        assert result is False


# ═══════════════════════════════════════════════════════════════════════════════
# Angle validation
# ═══════════════════════════════════════════════════════════════════════════════

class TestValidateAngle:
    """validate_angle checks angle is within 40°–85° range."""

    def test_angle_below_range_raises(self):
        """Angle below 40° should raise ValueError."""
        with pytest.raises(ValueError, match="outside the valid range"):
            validate_angle(39.0)

    def test_angle_above_range_raises(self):
        """Angle above 85° should raise ValueError."""
        with pytest.raises(ValueError, match="outside the valid range"):
            validate_angle(86.0)

    def test_angle_at_min_boundary_passes(self):
        """Angle at 40° should pass (boundary inclusive)."""
        validate_angle(40.0)  # Should not raise

    def test_angle_at_max_boundary_passes(self):
        """Angle at 85° should pass (boundary inclusive)."""
        validate_angle(85.0)  # Should not raise

    def test_angle_in_middle_passes(self, ruler_angle):
        """All test angles (40, 60, 85) should pass."""
        validate_angle(ruler_angle)  # Should not raise

    def test_invalid_angle_exact_min_minus_one(self):
        """39° is outside valid range."""
        with pytest.raises(ValueError):
            validate_angle(39.0)

    def test_invalid_angle_exact_max_plus_one(self):
        """86° is outside valid range."""
        with pytest.raises(ValueError):
            validate_angle(86.0)
