"""
Shared pytest fixtures for the Universal Filter Ruler test suite.

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


# ── Ruler preset fixtures ─────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def ruler_preset():
    """
    Return the Standard RulerPreset (200×120×8mm, ~350g).

    Use in tests that need the canonical design configuration.
    """
    from cad.params import STANDARD_PRESET
    return STANDARD_PRESET


@pytest.fixture(scope="session")
def travel_preset():
    """Return the Travel RulerPreset (150×90×8mm, ~250g)."""
    from cad.params import TRAVEL_PRESET
    return TRAVEL_PRESET


# ── Base plate parameter fixture ──────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_params():
    """
    Return a dict of base plate dimensional parameters sourced from cad.params.

    Keys mirror the vault spec section headers for traceability.
    """
    import cad.params as p
    return {
        "length_mm":     p.BASE_LENGTH_MM,
        "width_mm":      p.BASE_WIDTH_MM,
        "thickness_mm":  p.BASE_THICKNESS_MM,
        "flatness_mm":   p.BASE_FLATNESS_MM,
        "material":      p.BASE_MATERIAL,
        "treatment":     p.BASE_SURFACE_TREATMENT,
    }


# ── Arm angle parametric fixture ──────────────────────────────────────────────

@pytest.fixture(params=[40.0, 60.0, 85.0], ids=["40deg", "60deg", "85deg"])
def arm_angle(request):
    """
    Parametrized fixture supplying the three representative arm angles (degrees):
      - 40° — minimum setting (narrow cone)
      - 60° — mid-range (typical V60-style cone)
      - 85° — maximum setting (wide / shallow cone)

    Used in tests that must verify behaviour across the full operating range.
    """
    return request.param
