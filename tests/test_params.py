"""
Unit tests for cad/params.py — Universal Coffee Filter Ruler v3.0 parameter module.

Verifies:
  - Revision string (v3.0 tapered arms)
  - Arm dimensions (tapered trapezoidal profile)
  - Arc mark radii (V60 slant heights)
  - Angle system range (40°–85°)
  - Dripper presets (SD1R, SD1, V60, UFO)
  - Hardware specs (pivot bolt, washer, thumb screw)
  - Material specs and tolerances

No CadQuery required — pure data validation.
"""
import pytest
import cad.params as P


# ═══════════════════════════════════════════════════════════════════════════════
# Module import / revision
# ═══════════════════════════════════════════════════════════════════════════════

class TestModuleLoads:
    def test_importable(self):
        import cad.params  # noqa: F401

    def test_revision_is_string(self):
        assert isinstance(P.REVISION, str)
        assert len(P.REVISION) > 0

    def test_revision_is_3_0(self):
        assert P.REVISION == "3.0"


# ═══════════════════════════════════════════════════════════════════════════════
# Arm dimensions (tapered trapezoidal profile)
# ═══════════════════════════════════════════════════════════════════════════════

class TestArmDimensions:
    def test_count(self):
        assert P.ARM_COUNT == 2

    def test_length(self):
        assert P.ARM_LENGTH_MM == pytest.approx(120.0)

    def test_width_narrow(self):
        assert P.ARM_WIDTH_NARROW_MM == pytest.approx(25.0)

    def test_width_wide(self):
        assert P.ARM_WIDTH_WIDE_MM == pytest.approx(65.0)

    def test_thickness(self):
        assert P.ARM_THICKNESS_MM == pytest.approx(1.2)

    def test_edge_radius(self):
        """R0.3 mm comfort radius (laser cut + deburr)."""
        assert P.ARM_EDGE_RADIUS_MM == pytest.approx(0.3)

    def test_pivot_hole_diameter(self):
        assert P.ARM_PIVOT_HOLE_DIA_MM == pytest.approx(5.3)

    def test_pivot_hole_offset(self):
        assert P.ARM_PIVOT_HOLE_OFFSET_MM == pytest.approx(10.0)

    def test_material_is_ss304(self):
        assert "SS304" in P.ARM_MATERIAL or "304" in P.ARM_MATERIAL

    def test_surface_finish_brushed(self):
        assert "#4" in P.ARM_SURFACE_FINISH or "brushed" in P.ARM_SURFACE_FINISH.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# Arc marks (V60 slant heights)
# ═══════════════════════════════════════════════════════════════════════════════

class TestArcMarks:
    def test_01_radius(self):
        assert P.ARC_01_RADIUS_MM == pytest.approx(95.0)

    def test_02_radius(self):
        assert P.ARC_02_RADIUS_MM == pytest.approx(116.0)

    def test_03_radius(self):
        assert P.ARC_03_RADIUS_MM == pytest.approx(137.0)

    def test_arc_marks_dict_keys(self):
        assert set(P.ARC_MARKS.keys()) == {"01", "02", "03"}

    def test_arc_marks_dict_values_match_constants(self):
        assert P.ARC_MARKS["01"] == pytest.approx(P.ARC_01_RADIUS_MM)
        assert P.ARC_MARKS["02"] == pytest.approx(P.ARC_02_RADIUS_MM)
        assert P.ARC_MARKS["03"] == pytest.approx(P.ARC_03_RADIUS_MM)

    def test_arc_mark_ordering(self):
        """01 < 02 < 03 from pivot."""
        assert P.ARC_01_RADIUS_MM < P.ARC_02_RADIUS_MM < P.ARC_03_RADIUS_MM

    def test_arc_groove_dimensions(self):
        assert P.ARC_GROOVE_WIDTH_MM == pytest.approx(0.3)
        assert P.ARC_GROOVE_DEPTH_MM == pytest.approx(0.1)


# ═══════════════════════════════════════════════════════════════════════════════
# Angle system
# ═══════════════════════════════════════════════════════════════════════════════

class TestAngleSystem:
    def test_min_angle(self):
        assert P.ANGLE_MIN_DEG == pytest.approx(40.0)

    def test_max_angle(self):
        assert P.ANGLE_MAX_DEG == pytest.approx(85.0)

    def test_range(self):
        assert P.ANGLE_RANGE_DEG == pytest.approx(45.0)

    def test_default_angle(self):
        assert P.ANGLE_DEFAULT_DEG == pytest.approx(60.0)

    def test_tick_spacing(self):
        """Minor tick every 1°."""
        assert P.ANGLE_TICK_DEG == pytest.approx(1.0)

    def test_label_spacing(self):
        """Major (labeled) tick every 5°."""
        assert P.ANGLE_LABEL_DEG == pytest.approx(5.0)

    def test_min_less_than_max(self):
        assert P.ANGLE_MIN_DEG < P.ANGLE_MAX_DEG

    def test_range_exactly_45_degrees(self):
        assert (P.ANGLE_MAX_DEG - P.ANGLE_MIN_DEG) == pytest.approx(45.0)


# ═══════════════════════════════════════════════════════════════════════════════
# Dripper presets
# ═══════════════════════════════════════════════════════════════════════════════

class TestDripperPresets:
    def test_preset_keys(self):
        assert set(P.DRIPPER_PRESETS.keys()) == {"SD1R", "SD1", "V60", "UFO"}

    def test_v60_angle(self):
        assert P.DRIPPER_PRESETS["V60"] == pytest.approx(60.0)

    def test_sd1r_angle(self):
        assert P.DRIPPER_PRESETS["SD1R"] == pytest.approx(48.0)

    def test_sd1_angle(self):
        assert P.DRIPPER_PRESETS["SD1"] == pytest.approx(55.0)

    def test_ufo_angle(self):
        assert P.DRIPPER_PRESETS["UFO"] == pytest.approx(80.0)


# ═════════════════════════════════════════════════════════════════════════────══
# Pivot hardware
# ═══════════════════════════════════════════════════════════════════════════════

class TestPivotHardware:
    def test_bolt_spec_contains_m5(self):
        assert "M5" in P.PIVOT_BOLT_SPEC

    def test_bolt_diameter(self):
        assert P.PIVOT_BOLT_DIAMETER_MM == pytest.approx(5.0)

    def test_shoulder_diameter(self):
        assert P.PIVOT_SHOULDER_DIAMETER_MM == pytest.approx(8.0)

    def test_shoulder_length(self):
        assert P.PIVOT_SHOULDER_LENGTH_MM == pytest.approx(4.0)

    def test_bolt_head_diameter(self):
        assert P.PIVOT_BOLT_HEAD_DIA_MM == pytest.approx(10.0)

    def test_bolt_head_height(self):
        assert P.PIVOT_BOLT_HEAD_HEIGHT_MM == pytest.approx(3.0)


# ═══════════════════════════════════════════════════════════════════════════════
# PTFE Washer
# ═══════════════════════════════════════════════════════════════════════════════

class TestPTFEWasher:
    def test_washer_od(self):
        assert P.WASHER_OD_MM == pytest.approx(10.0)

    def test_washer_id(self):
        assert P.WASHER_ID_MM == pytest.approx(5.3)

    def test_washer_thickness(self):
        assert P.WASHER_THICKNESS_MM == pytest.approx(0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# Thumb screw
# ═══════════════════════════════════════════════════════════════════════════════

class TestThumbScrew:
    def test_head_diameter(self):
        assert P.THUMB_SCREW_HEAD_DIAMETER_MM == pytest.approx(15.0)

    def test_head_height(self):
        assert P.THUMB_SCREW_HEAD_HEIGHT_MM == pytest.approx(8.0)

    def test_shaft_diameter(self):
        assert P.THUMB_SCREW_SHAFT_DIAMETER_MM == pytest.approx(5.0)

    def test_shaft_length(self):
        assert P.THUMB_SCREW_SHAFT_LENGTH_MM == pytest.approx(8.0)

    def test_knurl_count(self):
        assert P.THUMB_SCREW_KNURL_COUNT == pytest.approx(12)


# ═══════════════════════════════════════════════════════════════════════════════
# Material specs (SS304)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMaterialSpecs:
    def test_ss304_density(self):
        assert P.SS304_DENSITY_G_PER_CM3 == pytest.approx(8.0)

    def test_arm_weight(self):
        assert P.ARM_WEIGHT_G == pytest.approx(51.8)

    def test_total_weight(self):
        # Total weight is calculated, allow small tolerance
        assert P.TOTAL_WEIGHT_G == pytest.approx(125.0, rel=0.01)


# ═══════════════════════════════════════════════════════════════════════════════
# Geometrical constraints (taper, ordering)
# ═══════════════════════════════════════════════════════════════════════════════

class TestGeometricalConstraints:
    def test_wide_greater_than_narrow(self):
        """Wide end must be wider than narrow end (taper check)."""
        assert P.ARM_WIDTH_WIDE_MM > P.ARM_WIDTH_NARROW_MM

    def test_arc_radii_ascending(self):
        """Arc radii must be in ascending order."""
        assert P.ARC_01_RADIUS_MM < P.ARC_02_RADIUS_MM < P.ARC_03_RADIUS_MM

    def test_arc_radii_within_arm_length_or_not(self):
        """Some arc marks may exceed arm length (they're skipped during build)."""
        # Just verify the values are defined correctly
        assert P.ARC_01_RADIUS_MM > 0
        assert P.ARC_02_RADIUS_MM > 0
        assert P.ARC_03_RADIUS_MM > 0


# ═══════════════════════════════════════════════════════════════════════════════
# Tolerances
# ═══════════════════════════════════════════════════════════════════════════════

class TestTolerances:
    def test_arm_length_tolerance(self):
        assert P.TOL_ARM_LENGTH_MM == pytest.approx(0.1)

    def test_arm_width_tolerance(self):
        assert P.TOL_ARM_WIDTH_MM == pytest.approx(0.05)

    def test_arm_thickness_tolerance(self):
        assert P.TOL_ARM_THICKNESS_MM == pytest.approx(0.05)

    def test_pivot_hole_tolerance(self):
        assert P.TOL_PIVOT_HOLE_MM == pytest.approx(0.02)

    def test_arc_mark_position_tolerance(self):
        assert P.TOL_ARC_MARK_POSITION_MM == pytest.approx(0.1)

    def test_angle_scale_tolerance(self):
        assert P.TOL_ANGLE_SCALE_DEG == pytest.approx(0.5)

    def test_edge_radius_tolerance(self):
        assert P.TOL_EDGE_RADIUS_MM == pytest.approx(0.1)

    def test_flatness_tolerance(self):
        assert P.TOL_FLATNESS_MM == pytest.approx(0.05)

    def test_general_linear_tolerance(self):
        assert P.TOL_LINEAR_MM == pytest.approx(0.1)
