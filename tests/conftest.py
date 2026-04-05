"""
Shared pytest fixtures for the conical-filter-shaper test suite.

CadQuery-dependent fixtures are skipped automatically when CQ is not installed
(use `pytest -m "not cq"` to run only pure-math tests in a CQ-less environment).
"""
import pytest
import importlib

# ── Availability markers ──────────────────────────────────────────────────────
try:
    import cadquery  # noqa: F401
    _HAS_CQ = True
except ImportError:
    _HAS_CQ = False

requires_cq = pytest.mark.skipif(not _HAS_CQ, reason="CadQuery not installed")


# ── Params fixture ────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def params():
    """Return the cad.params module."""
    import cad.params as p
    return p


# ── Preset fixtures ───────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def preset_p1(params):
    return params.PRESET_1

@pytest.fixture(scope="session")
def preset_p2(params):
    return params.PRESET_2

@pytest.fixture(scope="session")
def preset_p3(params):
    return params.PRESET_3

@pytest.fixture(params=["PRESET_1", "PRESET_2", "PRESET_3"], scope="session")
def any_preset(request, params):
    return getattr(params, request.param)


# ── Dripper profile fixture ───────────────────────────────────────────────────
@pytest.fixture(scope="session")
def dripper_profiles():
    from tests.fixtures.dripper_profiles import DRIPPER_PROFILES
    return DRIPPER_PROFILES
