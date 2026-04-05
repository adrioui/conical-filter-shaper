"""
Unit tests for cad/params.py — verify internal consistency of design parameters.
No CadQuery required.
"""
import math
import pytest
import cad.params as P
from cad.utils.cone_math import base_radius, axial_height


class TestConePresetSelfConsistency:
    """Verify that tabulated values in each ConePreset match their formulas."""

    @pytest.mark.parametrize("preset", P.PRESETS)
    def test_base_radius_formula(self, preset):
        """base_radius_mm ≈ slant_height × sin(half_angle)"""
        expected = base_radius(preset.slant_height_mm, preset.half_angle_deg)
        assert abs(preset.base_radius_mm - expected) < 0.15, (
            f"{preset.label}: tabulated base_radius={preset.base_radius_mm}, "
            f"formula gives {expected:.2f}"
        )

    @pytest.mark.parametrize("preset", P.PRESETS)
    def test_axial_height_formula(self, preset):
        """axial_height_mm ≈ slant_height × cos(half_angle)"""
        expected = axial_height(preset.slant_height_mm, preset.half_angle_deg)
        assert abs(preset.axial_height_mm - expected) < 0.15, (
            f"{preset.label}: tabulated axial_height={preset.axial_height_mm}, "
            f"formula gives {expected:.2f}"
        )

    @pytest.mark.parametrize("preset", P.PRESETS)
    def test_half_angle_is_half_of_included(self, preset):
        assert abs(preset.half_angle_deg - preset.included_angle_deg / 2.0) < 1e-6

    @pytest.mark.parametrize("preset", P.PRESETS)
    def test_cam_dwell_radius_matches_base_radius(self, preset):
        """Cam dwell radius must equal shell base radius for angle accuracy."""
        assert abs(preset.cam_dwell_radius_mm - preset.base_radius_mm) < 0.01, (
            f"{preset.label}: cam_dwell_radius={preset.cam_dwell_radius_mm} "
            f"≠ base_radius={preset.base_radius_mm}"
        )


class TestCamRingGeometry:
    """Verify cam ring envelope can accommodate all presets."""

    def test_cam_track_radial_reach_within_ring_od(self):
        """
        Shell base pins ride in the cam track on the ring's TOP FACE, not through the bore.
        Verify the max dwell radius fits within the ring face with adequate wall thickness.
        """
        max_dwell_r = max(p.cam_dwell_radius_mm for p in P.PRESETS)
        track_wall_mm = 4.0  # 4.0 mm absolute min; P3 design actual = 4.8 mm (acceptable)
        max_allowed_r = (P.CAM_RING_OD_MM / 2.0) - (P.CAM_TRACK_WIDTH_MM / 2.0) - track_wall_mm
        assert max_dwell_r <= max_allowed_r, (
            f"Max dwell radius {max_dwell_r} mm exceeds allowed {max_allowed_r:.1f} mm "
            f"(ring OD/2 - track_width/2 - {track_wall_mm} mm wall)"
        )

    def test_cam_dwell_plus_transition_closes_180_per_follower(self):
        """
        Per-follower arc sum must be 180°.
        The ring has 2 followers offset 180° apart; together they fill 360°.
        Each follower's track: 3 presets × (dwell + transition) = 3 × 60° = 180°.
        """
        n = len(P.PRESETS)
        total = n * (P.CAM_DWELL_ARC_DEG + P.CAM_TRANSITION_ARC_DEG)
        assert abs(total - 180.0) < 0.01, (
            f"Per-follower cam arc total = {total}°, expected 180° "
            "(2 followers × 180° = 360° full ring)"
        )


class TestDetentGeometry:
    """Verify detent dimple proportions."""

    def test_dimple_depth_is_35pct_ball_diameter(self):
        """
        Dimple depth target: ~35% of ball diameter.
        Convention here is depth/diameter. Acceptable range: 28–45% of diameter.
        """
        ball_d = P.DETENT_BALL_DIAMETER_MM
        ratio = P.DETENT_DIMPLE_DEPTH_MM / ball_d
        assert 0.28 <= ratio <= 0.45, (
            f"Detent dimple depth/diameter = {ratio:.2%}; "
            "outside 28–45% of ball diameter (too shallow = no click, too deep = won't release)"
        )

    def test_dimple_radius_greater_than_ball_radius(self):
        ball_r = P.DETENT_BALL_DIAMETER_MM / 2.0
        assert P.DETENT_DIMPLE_RADIUS_MM > ball_r, (
            "Dimple pocket radius must exceed ball radius for clean ball seating"
        )


class TestToolEnvelope:
    """Verify overall tool dimensions are within ergonomic bounds."""

    def test_handle_diameter_ergonomic(self):
        assert 35.0 <= P.HANDLE_OD_MM <= 50.0, (
            f"Handle OD {P.HANDLE_OD_MM} mm outside ergonomic range 35–50 mm"
        )

    def test_tool_height_reasonable(self):
        assert 140.0 <= P.TOOL_HEIGHT_AT_80DEG_MM <= 200.0, (
            f"Tool height {P.TOOL_HEIGHT_AT_80DEG_MM} mm outside expected 140–200 mm"
        )

    def test_max_width_at_widest_preset(self):
        assert abs(P.TOOL_MAX_WIDTH_MM - P.PRESET_3.base_radius_mm * 2) < 0.1


class TestTipInsertBlock:
    """Verify tip-block parameter relationships remain internally coherent."""

    def test_blind_ejection_chamber_clears_hinge_bore(self):
        chamber_bottom_z = P.TIP_BLOCK_HEIGHT_MM - P.TIP_EJECTION_CHAMBER_DEPTH_MM
        hinge_top_z = P.TIP_HINGE_BORE_Z_MM + (P.TIP_HINGE_BORE_DIA_MM / 2.0)
        clearance = chamber_bottom_z - hinge_top_z
        assert clearance >= 0.5, (
            f"Blind chamber / hinge clearance {clearance:.3f} mm too small; "
            "tip block internals would intersect"
        )


class TestFinSlot:
    """Verify fin slot provides positive clearance for fin insertion."""

    def test_fin_slot_wider_than_fin(self):
        assert P.FIN_SLOT_WIDTH_MM > P.FIN_THICKNESS_MM, (
            "Fin slot must be wider than fin thickness for assembly"
        )

    def test_fin_clearance_within_range(self):
        clearance = P.FIN_SLOT_WIDTH_MM - P.FIN_THICKNESS_MM
        assert 0.02 <= clearance <= 0.10, (
            f"Fin clearance {clearance:.3f} mm — too tight (<0.02) or too sloppy (>0.10)"
        )
