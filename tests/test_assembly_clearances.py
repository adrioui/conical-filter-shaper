"""Pure-params assembly clearance / stack-up checks."""
from __future__ import annotations

import cad.params as P


def test_axial_ring_stack_fits_housing_bore():
    stack_height = (2.0 * P.PTFE_WASHER_THICKNESS_MM) + P.CAM_RING_THICKNESS_MM
    bore_depth = P.HOUSING_FLANGE_HEIGHT_MM - P.HOUSING_RING_BORE_FLOOR_MM
    clearance = bore_depth - stack_height
    assert clearance >= 0.0, "ring + washer stack must fit within housing bore depth"
    assert clearance <= 1.0, "ring stack currently expects a very small nominal axial clearance"


def test_housing_bore_clearance_on_ring():
    diametral_clearance = P.HOUSING_RING_BORE_MM - P.CAM_RING_OD_MM
    assert 0.10 <= diametral_clearance <= 0.30, (
        f"Ring/housing diametral clearance {diametral_clearance:.3f} mm out of nominal range"
    )


def test_ejection_rod_reaches_button_design_path():
    """
    Design-intent stack check for the current nominal axial path.

    This is not proof of the present assembly placement; it is a source-of-truth length sanity
    check from the tip recess datum through the ring stack and housing body to the button end.
    """
    required_path = (
        P.EJECTION_ROD_RECESS_MM
        + P.PTFE_WASHER_THICKNESS_MM
        + P.CAM_RING_THICKNESS_MM
        + P.PTFE_WASHER_THICKNESS_MM
        + P.HOUSING_FLANGE_HEIGHT_MM
        + P.HANDLE_LENGTH_MM
    )
    assert P.EJECTION_ROD_LENGTH_MM >= required_path, (
        f"Ejection rod length {P.EJECTION_ROD_LENGTH_MM:.1f} mm is shorter than nominal path "
        f"{required_path:.1f} mm"
    )
