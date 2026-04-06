"""
Unit tests for cad/params.py — Universal Filter Ruler parameter module.

Verifies:
  - RulerPreset dataclass fields and values
  - Angle system range (40°–85°) and resolution constants
  - All critical dimensions against vault specifications
  - Material and process strings are non-empty and match spec keywords
  - Hardware and tolerance constants are present and sensible

No CadQuery required — pure data validation.
"""
import pytest
import cad.params as P
from cad.params import RulerPreset


# ═══════════════════════════════════════════════════════════════════════════════
# Module import / revision
# ═══════════════════════════════════════════════════════════════════════════════

class TestModuleLoads:
    def test_importable(self):
        import cad.params  # noqa: F401

    def test_revision_is_string(self):
        assert isinstance(P.REVISION, str)
        assert len(P.REVISION) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# RulerPreset dataclass
# ═══════════════════════════════════════════════════════════════════════════════

class TestRulerPresetDataclass:
    """RulerPreset is a frozen dataclass with the correct fields."""

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(RulerPreset)

    def test_is_frozen(self):
        """RulerPreset instances must be immutable."""
        preset = P.STANDARD_PRESET
        with pytest.raises((AttributeError, TypeError)):
            preset.name = "Modified"  # type: ignore[misc]

    def test_standard_preset_name(self):
        assert P.STANDARD_PRESET.name == "Standard"

    def test_travel_preset_name(self):
        assert P.TRAVEL_PRESET.name == "Travel"

    def test_standard_preset_dimensions(self):
        p = P.STANDARD_PRESET
        assert p.base_length_mm == 200.0
        assert p.base_width_mm == 120.0
        assert p.base_thickness_mm == 8.0

    def test_travel_preset_dimensions(self):
        p = P.TRAVEL_PRESET
        assert p.base_length_mm == 150.0
        assert p.base_width_mm == 90.0
        assert p.base_thickness_mm == 8.0   # Same thickness as Standard

    def test_standard_weight(self):
        assert P.STANDARD_PRESET.weight_g == pytest.approx(350.0)

    def test_travel_weight(self):
        assert P.TRAVEL_PRESET.weight_g == pytest.approx(250.0)

    def test_folded_height_both_presets(self):
        assert P.STANDARD_PRESET.folded_height_mm == pytest.approx(15.0)
        assert P.TRAVEL_PRESET.folded_height_mm == pytest.approx(15.0)

    def test_ruler_presets_list_contains_both(self):
        names = {p.name for p in P.RULER_PRESETS}
        assert "Standard" in names
        assert "Travel" in names

    def test_default_ruler_preset_is_standard(self):
        assert P.DEFAULT_RULER_PRESET.name == "Standard"


# ═══════════════════════════════════════════════════════════════════════════════
# Base plate dimensions  (vault: Design Specifications § Base Plate)
# ═══════════════════════════════════════════════════════════════════════════════

class TestBasePlateDimensions:
    def test_length(self):
        assert P.BASE_LENGTH_MM == pytest.approx(200.0)

    def test_width(self):
        assert P.BASE_WIDTH_MM == pytest.approx(120.0)

    def test_thickness(self):
        assert P.BASE_THICKNESS_MM == pytest.approx(8.0)

    def test_flatness_tolerance(self):
        """Flatness ≤ 0.05 mm over full length."""
        assert P.BASE_FLATNESS_MM == pytest.approx(0.05)

    def test_material_is_6061(self):
        assert "6061" in P.BASE_MATERIAL
        assert "T6" in P.BASE_MATERIAL or "T6" in P.BASE_MATERIAL


# ═══════════════════════════════════════════════════════════════════════════════
# T-Slot rails  (vault: CAD Design Brief § T-Slot Rails)
# ═══════════════════════════════════════════════════════════════════════════════

class TestTSlotRails:
    def test_count(self):
        assert P.TSLOT_COUNT == 2

    def test_opening_width(self):
        """Slot opening (top) = 6 mm."""
        assert P.TSLOT_OPENING_MM == pytest.approx(6.0)

    def test_undercut_width(self):
        """Undercut (wide part) = 10 mm."""
        assert P.TSLOT_UNDERCUT_MM == pytest.approx(10.0)

    def test_depth(self):
        """Slot depth = 5 mm."""
        assert P.TSLOT_DEPTH_MM == pytest.approx(5.0)

    def test_length(self):
        """Rail length = 180 mm."""
        assert P.TSLOT_LENGTH_MM == pytest.approx(180.0)

    def test_fit_class(self):
        assert "H7" in P.TSLOT_FIT_CLASS
        assert "h6" in P.TSLOT_FIT_CLASS


# ═══════════════════════════════════════════════════════════════════════════════
# Sliding arms  (vault: Design Specifications § Sliding Arms)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSlidingArms:
    def test_count(self):
        assert P.ARM_COUNT == 2

    def test_length(self):
        assert P.ARM_LENGTH_MM == pytest.approx(150.0)

    def test_width(self):
        assert P.ARM_WIDTH_MM == pytest.approx(25.0)

    def test_thickness(self):
        assert P.ARM_THICKNESS_MM == pytest.approx(6.0)

    def test_edge_radius(self):
        """R2.0 mm comfort radius on all external edges."""
        assert P.ARM_EDGE_RADIUS_MM == pytest.approx(2.0)

    def test_fold_guide_height(self):
        """Raised fold-guide edge = 3 mm."""
        assert P.ARM_FOLD_GUIDE_HEIGHT_MM == pytest.approx(3.0)

    def test_tslot_engagement(self):
        """T-tab engagement depth = 5 mm."""
        assert P.ARM_TSLOT_ENGAGEMENT_MM == pytest.approx(5.0)


# ═══════════════════════════════════════════════════════════════════════════════
# Angle system  (vault: Design Specifications § Angle Measurement System)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAngleSystem:
    def test_min_angle(self):
        assert P.ANGLE_MIN_DEG == pytest.approx(40.0)

    def test_max_angle(self):
        assert P.ANGLE_MAX_DEG == pytest.approx(85.0)

    def test_range(self):
        assert P.ANGLE_RANGE_DEG == pytest.approx(45.0)

    def test_primary_tick(self):
        """Minor (primary) tick every 1°."""
        assert P.ANGLE_PRIMARY_TICK_DEG == pytest.approx(1.0)

    def test_major_tick(self):
        """Major (labeled) tick every 5°."""
        assert P.ANGLE_MAJOR_TICK_DEG == pytest.approx(5.0)

    def test_vernier_resolution(self):
        """Vernier gives 0.5° resolution."""
        assert P.ANGLE_VERNIER_RESOLUTION_DEG == pytest.approx(0.5)

    def test_vernier_length(self):
        """Vernier scale window = 30 mm."""
        assert P.ANGLE_VERNIER_LENGTH_MM == pytest.approx(30.0)

    def test_accuracy_target(self):
        """Angle accuracy target ≤ ±0.1°."""
        assert P.ANGLE_ACCURACY_DEG <= 0.1

    def test_min_less_than_max(self):
        assert P.ANGLE_MIN_DEG < P.ANGLE_MAX_DEG

    def test_range_exactly_45_degrees(self):
        assert (P.ANGLE_MAX_DEG - P.ANGLE_MIN_DEG) == pytest.approx(45.0)


# ═══════════════════════════════════════════════════════════════════════════════
# Cam locks  (vault: Design Specifications § Cam Lock Mechanism)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCamLocks:
    def test_count(self):
        assert P.CAM_COUNT == 2

    def test_throw_angle(self):
        """Cam throw = 90° (quarter-turn)."""
        assert P.CAM_THROW_DEG == pytest.approx(90.0)

    def test_bolt_spec_is_m5(self):
        assert "M5" in P.CAM_BOLT_SPEC

    def test_material_is_ss316(self):
        assert "316" in P.CAM_MATERIAL

    def test_clamp_force(self):
        """Minimum clamping force = 50 N."""
        assert P.CAM_CLAMP_FORCE_N == pytest.approx(50.0)

    def test_lever_length(self):
        assert P.CAM_LEVER_LENGTH_MM == pytest.approx(25.0)


# ═══════════════════════════════════════════════════════════════════════════════
# Magnetic markers  (vault: Design Specifications § Magnetic Preset System)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMagneticMarkers:
    def test_total_count(self):
        assert P.MARKER_COUNT == 8

    def test_color_count(self):
        assert P.MARKER_COLOR_COUNT == 4

    def test_per_color(self):
        assert P.MARKER_PER_COLOR == 2

    def test_colors_list(self):
        assert len(P.MARKER_COLORS) == 4
        for color in ["Red", "Blue", "Green", "Yellow"]:
            assert color in P.MARKER_COLORS

    def test_count_equals_colors_times_per_color(self):
        assert P.MARKER_COUNT == P.MARKER_COLOR_COUNT * P.MARKER_PER_COLOR

    def test_diameter(self):
        assert P.MARKER_DIAMETER_MM == pytest.approx(6.0)

    def test_height(self):
        assert P.MARKER_HEIGHT_MM == pytest.approx(4.0)

    def test_magnet_grade_n52(self):
        assert "N52" in P.MARKER_MAGNET_GRADE

    def test_pull_force(self):
        """Pull force ≥ 0.5 kg."""
        assert P.MARKER_PULL_FORCE_KG >= 0.5


# ═══════════════════════════════════════════════════════════════════════════════
# Filter size guides  (vault: CAD Design Brief § Filter Size Guide Circles)
# ═══════════════════════════════════════════════════════════════════════════════

class TestFilterSizeGuides:
    def test_01_radius(self):
        """01 filter → R = 55 mm."""
        assert P.FILTER_01_RADIUS_MM == pytest.approx(55.0)

    def test_02_radius(self):
        """02 filter → R = 77.5 mm."""
        assert P.FILTER_02_RADIUS_MM == pytest.approx(77.5)

    def test_03_radius(self):
        """03 filter → R = 92.5 mm."""
        assert P.FILTER_03_RADIUS_MM == pytest.approx(92.5)

    def test_guides_dict_keys(self):
        assert set(P.FILTER_GUIDES.keys()) == {"01", "02", "03"}

    def test_guides_dict_values_match_constants(self):
        assert P.FILTER_GUIDES["01"] == pytest.approx(P.FILTER_01_RADIUS_MM)
        assert P.FILTER_GUIDES["02"] == pytest.approx(P.FILTER_02_RADIUS_MM)
        assert P.FILTER_GUIDES["03"] == pytest.approx(P.FILTER_03_RADIUS_MM)

    def test_radius_ordering(self):
        """01 < 02 < 03 in radius."""
        assert P.FILTER_01_RADIUS_MM < P.FILTER_02_RADIUS_MM < P.FILTER_03_RADIUS_MM


# ═══════════════════════════════════════════════════════════════════════════════
# Overlap scale  (vault: CAD Design Brief § Overlap Scale)
# ═══════════════════════════════════════════════════════════════════════════════

class TestOverlapScale:
    def test_min(self):
        assert P.OVERLAP_SCALE_MIN_MM == pytest.approx(0.0)

    def test_max(self):
        assert P.OVERLAP_SCALE_MAX_MM == pytest.approx(20.0)

    def test_tick_spacing(self):
        assert P.OVERLAP_SCALE_TICK_MM == pytest.approx(1.0)

    def test_label_interval(self):
        assert P.OVERLAP_SCALE_LABEL_INTERVAL_MM == pytest.approx(5.0)


# ═══════════════════════════════════════════════════════════════════════════════
# PTFE strips  (vault: BOM § PTFE Slide Strip)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPTFEStrips:
    def test_count(self):
        assert P.PTFE_COUNT == 2

    def test_length(self):
        assert P.PTFE_LENGTH_MM == pytest.approx(180.0)

    def test_width(self):
        assert P.PTFE_WIDTH_MM == pytest.approx(6.0)

    def test_thickness(self):
        assert P.PTFE_THICKNESS_MM == pytest.approx(0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# Assembly hardware  (vault: BOM)
# ═══════════════════════════════════════════════════════════════════════════════

class TestHardware:
    def test_m3_shcs_qty(self):
        assert P.FASTENER_M3_SHCS_QTY == 4

    def test_m3_shcs_spec(self):
        assert "M3" in P.FASTENER_M3_SHCS_SPEC

    def test_m5_shoulder_qty(self):
        assert P.FASTENER_M5_SHOULDER_QTY == 2

    def test_m5_shoulder_spec(self):
        assert "M5" in P.FASTENER_M5_SHOULDER_SPEC

    def test_belleville_qty(self):
        assert P.FASTENER_BELLEVILLE_QTY == 2

    def test_foot_pad_count(self):
        assert P.FOOT_PAD_COUNT == 4

    def test_foot_pad_diameter(self):
        assert P.FOOT_PAD_DIAMETER_MM == pytest.approx(8.0)

    def test_foot_pad_thickness(self):
        assert P.FOOT_PAD_THICKNESS_MM == pytest.approx(1.5)

    def test_foot_pad_material_silicone(self):
        assert "silicone" in P.FOOT_PAD_MATERIAL.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# Material specs  (vault: Design Specifications § Material Properties)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMaterialSpecs:
    def test_al6061_tensile_strength(self):
        """6061-T6: tensile ≥ 290 MPa."""
        assert P.AL6061_TENSILE_STRENGTH_MPA == pytest.approx(290.0)

    def test_al6061_yield_strength(self):
        """6061-T6: yield ≥ 240 MPa."""
        assert P.AL6061_YIELD_STRENGTH_MPA == pytest.approx(240.0)

    def test_al6061_density(self):
        """6061-T6: density = 2.7 g/cm³."""
        assert P.AL6061_DENSITY_G_CM3 == pytest.approx(2.7)

    def test_anodize_thickness_range(self):
        """Type III anodize: 25–50 µm."""
        lo, hi = P.ANODIZE_TYPE_III_THICKNESS_UM
        assert lo == pytest.approx(25.0)
        assert hi == pytest.approx(50.0)

    def test_anodize_hardness_range(self):
        """Type III anodize: 60–70 HRC."""
        lo, hi = P.ANODIZE_TYPE_III_HARDNESS_HRC
        assert lo == pytest.approx(60.0)
        assert hi == pytest.approx(70.0)

    def test_finish_matrix_has_all_components(self):
        expected = {"base_plate", "sliding_arm", "cam_body", "cam_lever",
                    "marker", "ferrous_strip"}
        assert expected.issubset(set(P.FINISH_MATRIX.keys()))

    def test_finish_matrix_values_nonempty(self):
        for key, value in P.FINISH_MATRIX.items():
            assert isinstance(value, str) and len(value) > 0, (
                f"FINISH_MATRIX['{key}'] is empty"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# Tolerances
# ═══════════════════════════════════════════════════════════════════════════════

class TestTolerances:
    def test_tslot_width_tolerance(self):
        assert P.TOL_TSLOT_WIDTH_MM == pytest.approx(0.02)

    def test_flatness_tolerance(self):
        assert P.TOL_FLATNESS_MM == pytest.approx(0.05)

    def test_angle_scale_tolerance(self):
        assert P.TOL_ANGLE_SCALE_DEG == pytest.approx(0.1)

    def test_general_linear_tolerance(self):
        assert P.TOL_LINEAR_MM == pytest.approx(0.1)
