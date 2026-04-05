"""
Component build tests.

These are scaffold-aware:
- if CadQuery is missing, they are skipped
- if a component is still intentionally stubbed, they are skipped
- once geometry exists, the same tests become smoke tests automatically
"""
import math
import pytest
from tests.conftest import requires_cq


def build_or_skip(builder, *args, **kwargs):
    try:
        return builder(*args, **kwargs)
    except NotImplementedError as exc:
        pytest.skip(f"component stub not implemented yet: {exc}")


@requires_cq
class TestComponentBuilds:
    """Smoke tests: implemented components must build without error."""

    @pytest.mark.parametrize("preset", [None], ids=["default_preset"])
    def test_shell_half_l_builds(self, params, preset):
        from cad.components.shell_half_l import build
        result = build_or_skip(build, params=params, preset=preset)
        assert result is not None

    @pytest.mark.parametrize("preset", [None], ids=["default_preset"])
    def test_shell_half_r_builds(self, params, preset):
        from cad.components.shell_half_r import build
        result = build_or_skip(build, params=params, preset=preset)
        assert result is not None

    def test_tip_insert_block_builds(self, params):
        from cad.components.tip_insert_block import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_cam_ring_builds(self, params):
        from cad.components.cam_ring import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_handle_housing_builds(self, params):
        from cad.components.handle_housing import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_handle_grip_insert_builds(self, params):
        from cad.components.handle_grip_insert import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_overlap_fin_builds(self, params):
        from cad.components.overlap_fin import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_ejection_rod_builds(self, params):
        from cad.components.ejection_rod import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_base_cap_builds(self, params):
        from cad.components.base_cap import build
        result = build_or_skip(build, params=params)
        assert result is not None


@requires_cq
class TestComponentBoundingBoxes:
    """Bounding box sanity checks on implemented components."""

    def test_tip_insert_block_bounding_box(self, params):
        from cad.components.tip_insert_block import build
        block = build_or_skip(build, params=params)
        bb = block.val().BoundingBox()
        assert abs(bb.xlen - params.TIP_BLOCK_WIDTH_MM) < 0.1
        assert abs(bb.ylen - params.TIP_BLOCK_DEPTH_MM) < 0.1
        assert abs(bb.zlen - params.TIP_BLOCK_HEIGHT_MM) < 0.1
        assert abs(bb.zmin) < 0.1

    def test_tip_insert_block_volume_reduced_from_plain_box(self, params):
        from cad.components.tip_insert_block import build
        block = build_or_skip(build, params=params)
        volume = block.val().Volume()
        plain_box = params.TIP_BLOCK_WIDTH_MM * params.TIP_BLOCK_DEPTH_MM * params.TIP_BLOCK_HEIGHT_MM
        assert volume < plain_box * 0.99, "dimple + bores should reduce tip-block volume"
        assert volume > plain_box * 0.90, "tip-block cuts should not over-remove material"

    def test_overlap_fin_bounding_box(self, params):
        from cad.components.overlap_fin import build
        fin = build_or_skip(build, params=params)
        bb = fin.val().BoundingBox()
        assert abs(bb.zlen - params.FIN_LENGTH_MM) < 0.1
        assert abs(bb.ylen - params.FIN_WIDTH_MM) < 0.1
        assert abs(bb.xlen - params.FIN_THICKNESS_MM) < 0.1

    def test_ejection_rod_bounding_box(self, params):
        from cad.components.ejection_rod import build
        rod = build_or_skip(build, params=params)
        bb = rod.val().BoundingBox()
        assert abs(bb.zlen - params.EJECTION_ROD_LENGTH_MM) < 0.5
        assert abs(bb.xlen - params.EJECTION_ROD_DIAMETER_MM) < 0.5
        assert abs(bb.ylen - params.EJECTION_ROD_DIAMETER_MM) < 0.5

    def test_base_cap_bounding_box(self, params):
        from cad.components.base_cap import build
        cap = build_or_skip(build, params=params)
        bb = cap.val().BoundingBox()
        assert abs(bb.xlen - params.BASE_CAP_OD_MM) < 0.5
        assert abs(bb.zlen - params.BASE_CAP_THICKNESS_MM) < 1.0

    def test_handle_housing_bounding_box(self, params):
        from cad.components.handle_housing import build
        housing = build_or_skip(build, params=params)
        bb = housing.val().BoundingBox()
        total = params.HOUSING_FLANGE_HEIGHT_MM + params.HANDLE_LENGTH_MM
        assert abs(bb.xlen - params.HOUSING_FLANGE_OD_MM) < 1.0
        assert abs(bb.ylen - params.HOUSING_FLANGE_OD_MM) < 1.0
        assert abs(bb.zlen - total) < 1.0
        assert abs(bb.zmax) < 0.1

    @pytest.mark.parametrize("preset_name", ["PRESET_1", "PRESET_2", "PRESET_3"])
    def test_shell_half_l_builds_all_presets(self, params, preset_name):
        from cad.components.shell_half_l import build
        preset = getattr(params, preset_name)
        result = build_or_skip(build, params=params, preset=preset)
        assert result is not None

    def test_shell_half_l_bounding_box_p2(self, params):
        from cad.components.shell_half_l import build
        shell = build_or_skip(build, params=params, preset=params.PRESET_2)
        bb = shell.val().BoundingBox()
        assert bb.zlen > (params.PRESET_2.axial_height_mm * 0.8)
        assert bb.zmax > params.PRESET_2.axial_height_mm
        assert bb.xlen > (params.SHELL_FOLLOWER_BOSS_OD_MM / 2.0)

    def test_cam_ring_od(self, params):
        from cad.components.cam_ring import build
        ring = build_or_skip(build, params=params)
        bb = ring.val().BoundingBox()
        ring_od = params.CAM_RING_OD_MM
        assert abs(bb.xmax - bb.xmin - ring_od) < 0.5
        assert abs(bb.ymax - bb.ymin - ring_od) < 0.5

    def test_cam_ring_thickness(self, params):
        from cad.components.cam_ring import build
        ring = build_or_skip(build, params=params)
        bb = ring.val().BoundingBox()
        thickness = params.CAM_RING_THICKNESS_MM
        assert abs(bb.zmax - bb.zmin - thickness) < 1.0

    def test_cam_ring_volume_reduced_from_plain_annulus(self, params):
        from cad.components.cam_ring import build
        ring = build_or_skip(build, params=params)
        volume = ring.val().Volume()
        plain_annulus = math.pi * (
            (params.CAM_RING_OD_MM / 2.0) ** 2 - (params.CAM_RING_BORE_MM / 2.0) ** 2
        ) * params.CAM_RING_THICKNESS_MM
        assert volume < plain_annulus * 0.99, "cam track + detent cuts should reduce volume"

    def test_cam_ring_volume_still_reasonable(self, params):
        from cad.components.cam_ring import build
        ring = build_or_skip(build, params=params)
        volume = ring.val().Volume()
        plain_annulus = math.pi * (
            (params.CAM_RING_OD_MM / 2.0) ** 2 - (params.CAM_RING_BORE_MM / 2.0) ** 2
        ) * params.CAM_RING_THICKNESS_MM
        assert volume > plain_annulus * 0.85, "cam-ring cuts should not over-remove material"
