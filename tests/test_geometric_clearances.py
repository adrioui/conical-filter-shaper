"""CadQuery-backed geometric assembly clearance / overlap checks.

These tests exercise actual built component geometry plus the current assembly placements.
A few checks are marked xfail(strict=True) to document known nominal-assembly issues without
pretending they are solved yet.
"""
from __future__ import annotations

import cadquery as cq
import pytest

from tests.conftest import requires_cq


_OVERLAP_TOLERANCE_MM3 = 1e-3


def _shape_in(assy, key: str):
    """Return a shape transformed by the composed assembly-location chain for `key`."""
    obj = assy.objects[key]
    parts = key.split("/")
    loc = cq.Location()
    if len(parts) > 1:
        prefix = ""
        for part in parts[:-1]:
            prefix = part if not prefix else f"{prefix}/{part}"
            loc = loc * assy.objects[prefix].loc
    loc = loc * obj.loc
    return obj.obj.val().located(loc)


def _overlap_volume(shape_a, shape_b) -> float:
    """Boolean-common overlap volume in mm³."""
    common = shape_a.intersect(shape_b)
    if common.isNull():
        return 0.0
    return abs(common.Volume())


@requires_cq
class TestGeometricAssemblyClearances:
    def test_ring_assy_cam_ring_clears_handle_housing(self, params):
        from cad.assemblies.ring_assy import build

        assy = build(params=params)
        housing = _shape_in(assy, "handle_housing")
        ring = _shape_in(assy, "cam_ring")
        overlap = _overlap_volume(housing, ring)
        assert overlap <= _OVERLAP_TOLERANCE_MM3, (
            f"Cam ring / handle housing overlap = {overlap:.6f} mm³"
        )

    def test_full_assy_base_cap_clears_handle_housing(self, params):
        from cad.assemblies.full_assy import build

        assy = build(params=params)
        housing = _shape_in(assy, "ring/handle_housing")
        cap = _shape_in(assy, "base_cap")
        overlap = _overlap_volume(housing, cap)
        assert overlap <= _OVERLAP_TOLERANCE_MM3, (
            f"Base cap / handle housing overlap = {overlap:.6f} mm³"
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Known nominal-assembly issue: grip insert currently overlaps the housing flange zone.",
    )
    def test_full_assy_grip_insert_clears_housing(self, params):
        from cad.assemblies.full_assy import build

        assy = build(params=params)
        housing = _shape_in(assy, "ring/handle_housing")
        grip = _shape_in(assy, "grip_insert")
        overlap = _overlap_volume(housing, grip)
        assert overlap <= _OVERLAP_TOLERANCE_MM3, (
            f"Grip insert / handle housing overlap = {overlap:.3f} mm³"
        )

    def test_mandrel_tip_block_clears_shell_halves(self, params):
        from cad.assemblies.mandrel_assy import build

        assy = build(params=params)
        tip_block = _shape_in(assy, "tip_insert_block")
        shell_l = _shape_in(assy, "shell_half_l")
        shell_r = _shape_in(assy, "shell_half_r")
        overlap_l = _overlap_volume(tip_block, shell_l)
        overlap_r = _overlap_volume(tip_block, shell_r)
        assert overlap_l <= _OVERLAP_TOLERANCE_MM3, (
            f"Tip block / shell_half_l overlap = {overlap_l:.3f} mm³"
        )
        assert overlap_r <= _OVERLAP_TOLERANCE_MM3, (
            f"Tip block / shell_half_r overlap = {overlap_r:.3f} mm³"
        )

    def test_full_assy_rod_clears_tip_block_at_rest(self, params):
        from cad.assemblies.full_assy import build

        assy = build(params=params)
        rod = _shape_in(assy, "ejection/rod")
        tip_block = _shape_in(assy, "mandrel/tip_insert_block")
        overlap = _overlap_volume(rod, tip_block)
        assert overlap <= _OVERLAP_TOLERANCE_MM3, (
            f"Ejection rod / tip block overlap = {overlap:.3f} mm³"
        )
