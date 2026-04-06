"""
Assembly build tests — Universal Filter Ruler.
Scaffold-aware like test_components.py.
"""
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

    def test_arm_assy_builds(self, params):
        from cad.assemblies.arm_assy import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_full_assy_builds(self, params):
        from cad.assemblies.full_assy import build
        result = build_or_skip(build, params=params)
        assert result is not None
