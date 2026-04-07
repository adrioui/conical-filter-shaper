"""
Shared pytest fixtures for the Universal Coffee Filter Ruler test suite.

CadQuery-dependent fixtures are skipped automatically when CQ is not installed.
Use ``pytest -m "not cq"`` to run only pure-math tests in a CQ-less environment.
"""
import pytest

# ── Availability markers ──────────────────────────────────────────────────────
try:
    import cadquery  # noqa: F401
    _HAS_CQ = True
except ImportError:
    _HAS_CQ = False

requires_cq = pytest.mark.skipif(not _HAS_CQ, reason="CadQuery not installed")


# ── Module fixture ────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def params():
    """Return the cad.params module (session-scoped — imported once per run)."""
    import cad.params as p
    return p


# ── Angle parametric fixture ──────────────────────────────────────────────────

@pytest.fixture(params=[40.0, 60.0, 85.0], ids=["40deg", "60deg", "85deg"])
def ruler_angle(request):
    """
    Parametrized fixture supplying three representative ruler angles (degrees):
      - 40° — minimum setting (narrow V)
      - 60° — mid-range (typical V60-style angle)
      - 85° — maximum setting (wide / shallow V)

    Used in tests that must verify behaviour across the full operating range.
    """
    return request.param
