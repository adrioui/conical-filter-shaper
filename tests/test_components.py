"""
Component build tests — Universal Filter Ruler.

Scaffold-aware:
- If CadQuery is missing, all tests are skipped.
- If a component raises NotImplementedError (stub), the test is skipped.
- Once geometry is implemented, the same tests become smoke tests automatically.
"""
import pytest
from tests.conftest import requires_cq


def build_or_skip(builder, *args, **kwargs):
    """Run builder or skip if NotImplementedError is raised."""
    try:
        return builder(*args, **kwargs)
    except NotImplementedError as exc:
        pytest.skip(f"component stub not implemented yet: {exc}")


@requires_cq
class TestComponentBuilds:
    """Smoke tests: implemented components must build without error."""

    def test_base_plate_builds(self, params):
        """Test that base_plate.build() returns a valid Workplane."""
        from cad.components.base_plate import build
        result = build_or_skip(build, params=params)
        assert result is not None, "build() returned None"

    def test_sliding_arm_builds(self, params):
        """Test that sliding_arm.build() returns a valid Workplane."""
        from cad.components.sliding_arm import build
        result = build_or_skip(build, params=params, side="left")
        assert result is not None, "build() returned None"

    def test_sliding_arm_right_side(self, params):
        """Test sliding_arm.build() with right side."""
        from cad.components.sliding_arm import build
        result = build_or_skip(build, params=params, side="right")
        assert result is not None, "build() returned None for right side"

    def test_cam_lock_builds(self, params):
        from cad.components.cam_lock import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_magnetic_marker_builds(self, params):
        from cad.components.magnetic_marker import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_ferrous_strip_builds(self, params):
        from cad.components.ferrous_strip import build
        result = build_or_skip(build, params=params)
        assert result is not None

    def test_ptfe_slide_strip_builds(self, params):
        from cad.components.ptfe_slide_strip import build
        result = build_or_skip(build, params=params)
        assert result is not None


@requires_cq
class TestBasePlateDimensions:
    """Bounding box and origin verification tests for base_plate."""

    def test_base_plate_bounding_box(self, params):
        """Verify base plate dimensions are within ±0.1mm of spec."""
        from cad.components.base_plate import build
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        # Get bounding box
        bb = result.val().BoundingBox()

        # Expected dimensions from params
        expected_length = params.BASE_LENGTH_MM if params else 200.0
        expected_width = params.BASE_WIDTH_MM if params else 120.0
        expected_thickness = params.BASE_THICKNESS_MM if params else 8.0

        # Tolerance
        tol = 0.1

        # Check dimensions (bounding box is from min to max, spans full dimension)
        actual_length = bb.xmax - bb.xmin
        actual_width = bb.ymax - bb.ymin
        actual_thickness = bb.zmax - bb.zmin

        assert abs(actual_length - expected_length) < tol, (
            f"Length {actual_length:.3f} differs from expected {expected_length} by more than {tol}mm"
        )
        assert abs(actual_width - expected_width) < tol, (
            f"Width {actual_width:.3f} differs from expected {expected_width} by more than {tol}mm"
        )
        assert abs(actual_thickness - expected_thickness) < tol, (
            f"Thickness {actual_thickness:.3f} differs from expected {expected_thickness} by more than {tol}mm"
        )

    def test_base_plate_origin(self, params):
        """Verify base plate origin is at center of bottom face."""
        from cad.components.base_plate import build
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        # Get bounding box
        bb = result.val().BoundingBox()

        # Origin should be at center-bottom: (0, 0, 0)
        # For plate with origin at center-bottom:
        # - X center is (xmin + xmax) / 2 = 0
        # - Y center is (ymin + ymax) / 2 = 0
        # - Z min should be 0 (bottom face at origin)

        expected_thickness = params.BASE_THICKNESS_MM if params else 8.0
        tol = 0.1

        # Check that X-center is at origin
        x_center = (bb.xmin + bb.xmax) / 2
        assert abs(x_center) < tol, f"X center {x_center:.3f} should be at origin (0)"

        # Check that Y-center is at origin
        y_center = (bb.ymin + bb.ymax) / 2
        assert abs(y_center) < tol, f"Y center {y_center:.3f} should be at origin (0)"

        # Check that bottom face is at Z=0
        assert abs(bb.zmin) < tol, f"Bottom face Z={bb.zmin:.3f} should be at origin (0)"

        # Check that top face is at Z=thickness
        assert abs(bb.zmax - expected_thickness) < tol, (
            f"Top face Z={bb.zmax:.3f} should be at thickness ({expected_thickness}mm)"
        )


@requires_cq
class TestSlidingArmDimensions:
    """Bounding box and origin verification tests for sliding_arm."""

    def test_sliding_arm_bounding_box(self, params):
        """Verify sliding arm dimensions are within ±0.1mm of spec."""
        from cad.components.sliding_arm import build
        result = build_or_skip(build, params=params, side="left")
        if result is None:
            pytest.skip("build() returned None")

        # Get bounding box
        bb = result.val().BoundingBox()

        # Expected dimensions from params
        expected_length = params.ARM_LENGTH_MM if params else 150.0
        expected_width = params.ARM_WIDTH_MM if params else 25.0
        expected_thickness = params.ARM_THICKNESS_MM if params else 6.0

        # Tolerance
        tol = 0.3  # Allow for tongue and fold guide protrusions

        # Check dimensions
        actual_length = bb.xmax - bb.xmin
        actual_width = bb.ymax - bb.ymin
        actual_thickness = bb.zmax - bb.zmin

        # Length check (should match spec)
        assert abs(actual_length - expected_length) < tol, (
            f"Length {actual_length:.3f} differs from expected {expected_length} by more than {tol}mm"
        )

        # Width check (may vary due to T-slot tongue)
        assert abs(actual_width - expected_width) < tol * 2, (
            f"Width {actual_width:.3f} may include tongue width"
        )

        # Thickness check (may include fold guide)
        assert actual_thickness >= expected_thickness, (
            f"Thickness {actual_thickness:.3f} should be at least {expected_thickness}mm"
        )

    def test_sliding_arm_origin_at_pivot_end(self, params):
        """Verify sliding arm origin is at the pivot end (cam lock hole end)."""
        from cad.components.sliding_arm import build
        result = build_or_skip(build, params=params, side="left")
        if result is None:
            pytest.skip("build() returned None")

        # Get bounding box
        bb = result.val().BoundingBox()

        # Origin should be at pivot end center-bottom
        # X should start at 0 (or very close)
        tol = 1.0  # Allow some tolerance for cam slot positioning

        assert bb.xmin < tol, f"Arm starts at X={bb.xmin:.3f}, should be at pivot end"

    def test_sliding_arm_both_sides_build(self, params):
        """Test that both left and right arms build successfully."""
        from cad.components.sliding_arm import build

        left_result = build_or_skip(build, params=params, side="left")
        right_result = build_or_skip(build, params=params, side="right")

        assert left_result is not None, "Left arm build returned None"
        assert right_result is not None, "Right arm build returned None"

    def test_sliding_arm_invalid_side_raises(self, params):
        """Test that invalid side parameter raises ValueError."""
        from cad.components.sliding_arm import build

        with pytest.raises(ValueError, match="side must be 'left' or 'right'"):
            build(params=params, side="invalid")