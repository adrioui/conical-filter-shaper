"""
Cam track geometry tests.
Verifies dwell radii, arc sums, and sinusoidal transition smoothness.
No CadQuery required.
"""
import math
import pytest
import cad.params as P
from cad.utils.cam_geometry import build_cam_track, sinusoidal_transition


class TestSinusoidalTransition:

    def test_starts_at_start_radius(self):
        radii = sinusoidal_transition(33.3, 41.0, n_points=64)
        assert abs(radii[0] - 33.3) < 1e-6

    def test_ends_at_end_radius(self):
        radii = sinusoidal_transition(33.3, 41.0, n_points=64)
        assert abs(radii[-1] - 41.0) < 1e-6

    def test_monotonic_increasing(self):
        radii = sinusoidal_transition(33.3, 41.0, n_points=64)
        for i in range(len(radii) - 1):
            assert radii[i] <= radii[i + 1] + 1e-9, f"Non-monotonic at index {i}"

    def test_monotonic_decreasing(self):
        radii = sinusoidal_transition(52.7, 33.3, n_points=64)
        for i in range(len(radii) - 1):
            assert radii[i] >= radii[i + 1] - 1e-9, f"Non-monotonic at index {i}"


class TestCamTrackClosure:

    def test_per_follower_track_spans_180(self):
        """
        Each follower's track spans 180° (half-rotation covers all 3 presets).
        Two followers at 0° and 180° offset together fill the full 360°.
        """
        n = len(P.PRESETS)
        expected_span = n * (P.CAM_DWELL_ARC_DEG + P.CAM_TRANSITION_ARC_DEG)
        assert abs(expected_span - 180.0) < 0.01, (
            f"Per-follower track span = {expected_span}°; expected 180°"
        )


class TestDwellRadii:

    def test_dwell_radii_match_presets(self):
        """Dwell radii in cam track must match ConePreset.cam_dwell_radius_mm."""
        dwell_radii = [p.cam_dwell_radius_mm for p in P.PRESETS]
        track = build_cam_track(
            dwell_radii=dwell_radii,
            dwell_arc_deg=P.CAM_DWELL_ARC_DEG,
            transition_arc_deg=P.CAM_TRANSITION_ARC_DEG,
        )
        # Collect the radius at the midpoint of each expected dwell zone
        expected_dwells = [33.3, 41.0, 52.7]
        mid_angles = [
            P.CAM_DWELL_ARC_DEG / 2,
            P.CAM_DWELL_ARC_DEG / 2 + (P.CAM_DWELL_ARC_DEG + P.CAM_TRANSITION_ARC_DEG),
            P.CAM_DWELL_ARC_DEG / 2 + 2 * (P.CAM_DWELL_ARC_DEG + P.CAM_TRANSITION_ARC_DEG),
        ]
        for expected_r, target_angle in zip(expected_dwells, mid_angles):
            # Find the point closest to target_angle
            closest = min(track, key=lambda pt: abs(pt.angle_deg - target_angle))
            assert abs(closest.radius_mm - expected_r) < 0.5, (
                f"At dwell midpoint ~{target_angle}°: expected r={expected_r} mm, "
                f"got {closest.radius_mm:.2f} mm"
            )
