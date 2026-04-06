"""
Tolerance / fit tests — verify that ISO 286 fit clearances are in the correct range.
Uses cad/utils/tolerances.py (pure math, no CadQuery required).

Fits tested here correspond to the Universal Filter Ruler T-slot mechanism.
"""
import pytest
from cad.utils.tolerances import get_fit


class TestSlidingFits:
    """T-slot arm sliding fit."""

    def test_tslot_arm_H7_h6(self):
        """
        T-slot arm engagement (3 mm reference): must be a light sliding fit.
        H7/h6 → clearance-only, max clearance ≤ 0.025 mm (per design spec).
        """
        fit = get_fit(3.0, "H7", "h6")
        assert fit.is_clearance_fit, "T-slot arm fit must be clearance (not interference)"
        assert fit.min_clearance_mm >= 0.0
        assert fit.max_clearance_mm <= 0.025

    def test_cam_pivot_H7_f7(self):
        """
        Cam lock pivot (3 mm reference): running clearance, 0.010–0.030 mm.
        """
        fit = get_fit(3.0, "H7", "f7")
        assert fit.is_clearance_fit
        assert fit.min_clearance_mm >= 0.008
        assert fit.max_clearance_mm <= 0.035


class TestInterferenceFits:

    def test_cam_pin_H7_n6(self):
        """Cam eccentric pin (4 mm) must be interference fit in housing bore."""
        fit = get_fit(4.0, "H7", "n6")
        assert fit.is_interference_fit, (
            f"Cam pin fit must be interference; "
            f"min clearance = {fit.min_clearance_mm:.4f} mm (should be negative)"
        )
