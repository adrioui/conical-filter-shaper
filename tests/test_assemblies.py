"""
Assembly build tests — Universal Coffee Filter Ruler v3.0.
Tests for ruler_assy with angle range validation.
"""
from __future__ import annotations

import pytest
from tests.conftest import requires_cq


def build_or_skip(builder, *args, **kwargs):
    """Call builder, skip test if NotImplementedError is raised."""
    try:
        return builder(*args, **kwargs)
    except NotImplementedError as exc:
        pytest.skip(f"assembly stub not implemented yet: {exc}")


# ═══════════════════════════════════════════════════════════════════════════════
# RULER ASSEMBLY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@requires_cq
class TestRulerAssembly:

    def test_ruler_assy_builds_at_60_deg(self, params):
        """Ruler assembly should build at default angle (60°)."""
        from cad.assemblies.ruler_assy import build
        result = build_or_skip(build, params=params, angle_deg=60.0)
        assert result is not None

    def test_ruler_assy_builds_at_40_deg(self, params):
        """Ruler assembly should build at minimum angle (40°)."""
        from cad.assemblies.ruler_assy import build
        result = build_or_skip(build, params=params, angle_deg=40.0)
        assert result is not None

    def test_ruler_assy_builds_at_85_deg(self, params):
        """Ruler assembly should build at maximum angle (85°)."""
        from cad.assemblies.ruler_assy import build
        result = build_or_skip(build, params=params, angle_deg=85.0)
        assert result is not None

    def test_ruler_assy_invalid_angle_below_raises(self, params):
        """Angle below minimum should raise ValueError."""
        from cad.assemblies.ruler_assy import build
        with pytest.raises(ValueError, match="angle_deg must be between"):
            build(params=params, angle_deg=30.0)

    def test_ruler_assy_invalid_angle_above_raises(self, params):
        """Angle above maximum should raise ValueError."""
        from cad.assemblies.ruler_assy import build
        with pytest.raises(ValueError, match="angle_deg must be between"):
            build(params=params, angle_deg=90.0)


# ═══════════════════════════════════════════════════════════════════════════════
# ANGLE VALIDATION (no CQ needed — validation happens before geometry)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAngleValidation:
    """Angle range checks work even without CadQuery."""

    def test_angle_below_range_raises(self):
        from cad.assemblies.ruler_assy import build
        with pytest.raises(ValueError, match="angle_deg must be between"):
            build(angle_deg=39.0)

    def test_angle_above_range_raises(self):
        from cad.assemblies.ruler_assy import build
        with pytest.raises(ValueError, match="angle_deg must be between"):
            build(angle_deg=86.0)

    def test_angle_at_min_boundary(self):
        """40.0° is valid — should build successfully."""
        from cad.assemblies.ruler_assy import build
        result = build(angle_deg=40.0)
        assert result is not None

    def test_angle_at_max_boundary(self):
        """85.0° is valid — should build successfully."""
        from cad.assemblies.ruler_assy import build
        result = build(angle_deg=85.0)
        assert result is not None
