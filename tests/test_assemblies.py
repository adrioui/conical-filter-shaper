"""Assembly build tests — scaffold-aware like test_components.py."""
from __future__ import annotations

import pytest
from tests.conftest import requires_cq


def build_or_skip(builder, *args, **kwargs):
    try:
        return builder(*args, **kwargs)
    except NotImplementedError as exc:
        pytest.skip(f"assembly stub not implemented yet: {exc}")


@requires_cq
class TestAssemblyBuilds:
    def test_ejection_assy_builds(self, params):
        from cad.assemblies.ejection_assy import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_ring_assy_builds(self, params):
        from cad.assemblies.ring_assy import build
        result = build_or_skip(build, params=params)
        assert result is not None

    @pytest.mark.parametrize("preset", [None], ids=["default_preset"])
    def test_mandrel_assy_builds(self, params, preset):
        from cad.assemblies.mandrel_assy import build
        result = build_or_skip(build, params=params, preset=preset)
        assert result is not None

    @pytest.mark.parametrize("preset", [None], ids=["default_preset"])
    def test_full_assy_builds(self, params, preset):
        from cad.assemblies.full_assy import build
        result = build_or_skip(build, params=params, preset=preset)
        assert result is not None
