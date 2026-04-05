"""
Tolerance / fit tests — verify that ISO fit clearances are in the correct range.
No CadQuery required.
"""
import pytest
from cad.utils.tolerances import get_fit


class TestSlidingFits:

    def test_ejection_rod_H7_h6(self):
        """Ejection rod (3 mm) must be a light sliding fit with no interference."""
        fit = get_fit(3.0, "H7", "h6")
        assert fit.is_clearance_fit, "Ejection rod fit must be clearance (not interference)"
        assert fit.min_clearance_mm >= 0.0
        assert fit.max_clearance_mm <= 0.025

    def test_hinge_pin_H7_f7(self):
        """Hinge pin (3 mm) pivot clearance: 0.010–0.030 mm."""
        fit = get_fit(3.0, "H7", "f7")
        assert fit.is_clearance_fit
        assert fit.min_clearance_mm >= 0.008
        assert fit.max_clearance_mm <= 0.035


class TestInterferenceFits:

    def test_follower_pin_H7_n6_in_POM(self):
        """Cam follower pin (4 mm) must be interference fit in POM boss."""
        fit = get_fit(4.0, "H7", "n6")
        assert fit.is_interference_fit, (
            f"Follower pin fit must be interference; "
            f"min clearance = {fit.min_clearance_mm:.4f} mm (should be negative)"
        )
