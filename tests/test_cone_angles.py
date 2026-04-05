"""
Angle accuracy tests — verify that the cam dwell radii produce correct included angles
within the ANGLE_ACCURACY_TARGET_DEG tolerance.
No CadQuery required.
"""
import pytest
import cad.params as P
from cad.utils.cone_math import included_angle_from_radii


@pytest.mark.parametrize("preset", P.PRESETS, ids=[p.label for p in P.PRESETS])
def test_angle_back_calculation(preset):
    """
    Back-calculate the included angle from the tabulated base radius and slant height.
    Must be within ANGLE_ACCURACY_TARGET_DEG of the nominal angle.
    """
    recovered = included_angle_from_radii(preset.base_radius_mm, preset.slant_height_mm)
    error = abs(recovered - preset.included_angle_deg)
    assert error <= P.ANGLE_ACCURACY_TARGET_DEG, (
        f"{preset.label}: recovered angle={recovered:.3f}°, "
        f"nominal={preset.included_angle_deg}°, error={error:.3f}° "
        f"(limit ±{P.ANGLE_ACCURACY_TARGET_DEG}°)"
    )


@pytest.mark.parametrize("preset", P.PRESETS, ids=[p.label for p in P.PRESETS])
def test_cam_dwell_radius_produces_correct_angle(preset):
    """
    The cam_dwell_radius_mm is what the physical cam track delivers.
    Verify it produces the correct cone angle.
    """
    recovered = included_angle_from_radii(preset.cam_dwell_radius_mm, preset.slant_height_mm)
    error = abs(recovered - preset.included_angle_deg)
    assert error <= P.ANGLE_ACCURACY_TARGET_DEG, (
        f"{preset.label}: cam_dwell_radius={preset.cam_dwell_radius_mm} mm → "
        f"angle={recovered:.3f}°, expected {preset.included_angle_deg}°"
    )


def test_preset_angles_are_distinct():
    """The three presets must differ by more than the accuracy target."""
    angles = [p.included_angle_deg for p in P.PRESETS]
    for i in range(len(angles)):
        for j in range(i + 1, len(angles)):
            diff = abs(angles[i] - angles[j])
            assert diff > 2 * P.ANGLE_ACCURACY_TARGET_DEG, (
                f"Presets {i} and {j} are too close: {angles[i]}° vs {angles[j]}°"
            )


def test_worst_case_tolerance_stack():
    """
    Tolerance stack analysis (spec §6.2):
    Worst-case linear sum of all angle error sources must be ≤ ANGLE_ACCURACY_TARGET_DEG.

    Sources:
        Cam track radius: ±0.10 mm
        Follower pin play in track: ±0.05 mm
        Slant length variation: ±0.20 mm (→ angle error via derivative)
        Hinge pin lateral play: ±0.02 mm
    """
    import math

    slant = P.PRESET_1.slant_height_mm
    half_angle_rad = math.radians(P.PRESET_1.half_angle_deg)

    # Angle sensitivity to base radius: d(included_angle)/dr = 2 / sqrt(L² - r²) [rad/mm]
    r = P.PRESET_1.base_radius_mm
    dangle_dr_rad_per_mm = 2.0 / math.sqrt(slant**2 - r**2)  # ×2 for included angle
    dangle_dr_deg_per_mm = math.degrees(dangle_dr_rad_per_mm)

    cam_track_error_deg = 0.10 * dangle_dr_deg_per_mm
    follower_play_deg   = 0.05 * dangle_dr_deg_per_mm
    slant_error_deg     = 0.20 * math.degrees(math.sin(half_angle_rad) / slant)  # approximate
    hinge_play_deg      = 0.02 * dangle_dr_deg_per_mm

    worst_case_linear = cam_track_error_deg + follower_play_deg + slant_error_deg + hinge_play_deg

    assert worst_case_linear <= P.ANGLE_ACCURACY_TARGET_DEG, (
        f"Worst-case tolerance stack = ±{worst_case_linear:.3f}° exceeds target "
        f"±{P.ANGLE_ACCURACY_TARGET_DEG}°. Review tolerance groups in params.py."
    )
