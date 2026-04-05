"""
ISO 286 tolerance helpers.
Returns upper and lower deviations (mm) for common fits used in this project.
Pure math — no CadQuery imports.

Reference: ISO 286-1:2010, tables for Ø 1–500 mm.
Only the fits actually used in this project are implemented here.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class FitResult:
    nominal_mm: float
    hole_upper_mm: float   # Upper deviation from nominal (positive = larger)
    hole_lower_mm: float
    shaft_upper_mm: float
    shaft_lower_mm: float

    @property
    def min_clearance_mm(self) -> float:
        """Positive = clearance, negative = interference."""
        return self.hole_lower_mm - self.shaft_upper_mm

    @property
    def max_clearance_mm(self) -> float:
        return self.hole_upper_mm - self.shaft_lower_mm

    @property
    def is_clearance_fit(self) -> bool:
        return self.min_clearance_mm >= 0.0

    @property
    def is_interference_fit(self) -> bool:
        return self.max_clearance_mm <= 0.0


# Simplified lookup for nominal diameters used in this project.
# Format: {(nominal_mm, fit_code): (upper_dev_mm, lower_dev_mm)}
# Positive deviation = bore/shaft is LARGER than nominal.

_SHAFT_DEVIATIONS: dict[tuple[float, str], tuple[float, float]] = {
    # (nominal_mm, fit) : (upper, lower)  — shaft
    (3.0, "h6"):  ( 0.000, -0.006),
    (3.0, "f7"):  (-0.010, -0.022),
    (3.0, "n6"):  (+0.016, +0.010),
    (4.0, "h6"):  ( 0.000, -0.008),
    (4.0, "f7"):  (-0.010, -0.022),
    (4.0, "n6"):  (+0.020, +0.012),
}

_HOLE_DEVIATIONS: dict[tuple[float, str], tuple[float, float]] = {
    # (nominal_mm, fit) : (upper, lower)  — hole/bore
    (3.0, "H7"):  (+0.010, 0.000),
    (4.0, "H7"):  (+0.012, 0.000),
    (4.0, "H7p"): (+0.025, 0.000),  # wider H7 for POM bore (thermal expansion)
}


def get_fit(nominal_mm: float, hole_fit: str, shaft_fit: str) -> FitResult:
    """
    Return deviation data for a given fit pair.

    Example:
        fit = get_fit(3.0, "H7", "h6")
        print(fit.min_clearance_mm)  # sliding fit clearance
    """
    h_key = (nominal_mm, hole_fit)
    s_key = (nominal_mm, shaft_fit)
    if h_key not in _HOLE_DEVIATIONS:
        raise KeyError(f"Hole fit {hole_fit} at ø{nominal_mm} not in table. Add to tolerances.py.")
    if s_key not in _SHAFT_DEVIATIONS:
        raise KeyError(f"Shaft fit {shaft_fit} at ø{nominal_mm} not in table. Add to tolerances.py.")

    hu, hl = _HOLE_DEVIATIONS[h_key]
    su, sl = _SHAFT_DEVIATIONS[s_key]
    return FitResult(nominal_mm, hu, hl, su, sl)
