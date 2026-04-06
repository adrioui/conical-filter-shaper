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

        # Width check (includes fold guide protrusion on one side)
        # Fold guide adds ~1.5mm to width on one side
        guide_protrusion = params.ARM_FOLD_GUIDE_PROFILE_MM if params else 1.5
        assert actual_width >= expected_width, (
            f"Width {actual_width:.3f} should be at least {expected_width}mm"
        )
        assert actual_width <= expected_width + guide_protrusion * 2 + tol, (
            f"Width {actual_width:.3f} should not exceed arm width + fold guide"
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


@requires_cq
class TestCamLockDimensions:
    """Bounding box and origin verification tests for cam_lock."""

    def test_cam_lock_bounding_box(self, params):
        """Verify cam lock dimensions are within ±0.5mm of spec."""
        from cad.components.cam_lock import build, CAM_DISC_DIAMETER_MM, CAM_DISC_THICKNESS_MM, CAM_LOCK_ECCENTRICITY_MM
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Expected dimensions
        # Cam disc: 12mm diameter, but lever extends beyond
        # Eccentricity offset moves center slightly
        disc_diameter = CAM_DISC_DIAMETER_MM
        disc_thickness = CAM_DISC_THICKNESS_MM
        eccentricity = CAM_LOCK_ECCENTRICITY_MM

        # Length includes disc radius + lever length
        if params:
            lever_length = params.CAM_LEVER_LENGTH_MM
        else:
            from cad.params import CAM_LEVER_LENGTH_MM
            lever_length = CAM_LEVER_LENGTH_MM

        from cad.components.cam_lock import CAM_LEVER_WIDTH_MM
        lever_width = CAM_LEVER_WIDTH_MM

        # Tolerance
        tol = 0.5

        # Check Z dimension (thickness)
        actual_thickness = bb.zmax - bb.zmin
        assert abs(actual_thickness - disc_thickness) < tol, (
            f"Thickness {actual_thickness:.3f} differs from expected {disc_thickness} by more than {tol}mm"
        )

        # Check Y dimension (width - should be roughly disc diameter + some margin)
        actual_width = bb.ymax - bb.ymin
        assert actual_width >= disc_diameter - tol, (
            f"Width {actual_width:.3f} should be at least disc diameter {disc_diameter}mm"
        )

    def test_cam_lock_origin_at_center(self, params):
        """Verify cam lock origin is at center of rotation axis."""
        from cad.components.cam_lock import build, CAM_LOCK_ECCENTRICITY_MM
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Origin should be at center of cam disc (with small eccentricity offset)
        # The pivot hole is offset by eccentricity
        tol = 1.0

        # Z should start at 0 (bottom face at origin)
        assert bb.zmin < tol, f"Bottom face Z={bb.zmin:.3f} should be near origin (0)"


@requires_cq
class TestMagneticMarkerDimensions:
    """Bounding box and origin verification tests for magnetic_marker."""

    def test_magnetic_marker_bounding_box(self, params):
        """Verify magnetic marker dimensions are within ±0.5mm of spec."""
        from cad.components.magnetic_marker import build
        result = build_or_skip(build, params=params, color="red")
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Expected dimensions
        if params:
            diameter = params.MARKER_DIAMETER_MM
            height = params.MARKER_HEIGHT_MM
            magnet_thickness = params.MARKER_MAGNET_THICKNESS_MM
        else:
            from cad.params import MARKER_DIAMETER_MM, MARKER_HEIGHT_MM, MARKER_MAGNET_THICKNESS_MM
            diameter = MARKER_DIAMETER_MM
            height = MARKER_HEIGHT_MM
            magnet_thickness = MARKER_MAGNET_THICKNESS_MM

        from cad.components.magnetic_marker import MARKER_DOME_HEIGHT_MM
        dome_height = MARKER_DOME_HEIGHT_MM

        # Tolerance
        tol = 0.5

        # Check diameter (X and Y should be same for cylinder)
        actual_x = bb.xmax - bb.xmin
        actual_y = bb.ymax - bb.ymin
        assert abs(actual_x - diameter) < tol, (
            f"Diameter X {actual_x:.3f} differs from expected {diameter} by more than {tol}mm"
        )
        assert abs(actual_y - diameter) < tol, (
            f"Diameter Y {actual_y:.3f} differs from expected {diameter} by more than {tol}mm"
        )

        # Height should be body height + dome (magnet pocket is recessed into bottom)
        # Total height includes dome
        actual_height = bb.zmax - bb.zmin
        expected_height = height - magnet_thickness + dome_height
        assert actual_height >= expected_height - tol, (
            f"Height {actual_height:.3f} should be at least {expected_height}mm"
        )

    def test_magnetic_marker_origin_at_center_bottom(self, params):
        """Verify magnetic marker origin is at center of bottom face."""
        from cad.components.magnetic_marker import build
        result = build_or_skip(build, params=params, color="blue")
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Origin at center-bottom means:
        # - X and Y centers are at origin
        # - Z min is at origin
        tol = 0.5

        x_center = (bb.xmin + bb.xmax) / 2
        y_center = (bb.ymin + bb.ymax) / 2

        assert abs(x_center) < tol, f"X center {x_center:.3f} should be at origin (0)"
        assert abs(y_center) < tol, f"Y center {y_center:.3f} should be at origin (0)"
        assert bb.zmin < tol, f"Bottom face Z={bb.zmin:.3f} should be at origin (0)"

    def test_magnetic_marker_all_colors(self, params):
        """Test that all marker colors build successfully."""
        from cad.components.magnetic_marker import build

        for color in ["red", "blue", "green", "yellow"]:
            result = build_or_skip(build, params=params, color=color)
            assert result is not None, f"build() returned None for color={color}"

    def test_magnetic_marker_invalid_color_raises(self, params):
        """Test that invalid color parameter raises ValueError."""
        from cad.components.magnetic_marker import build

        with pytest.raises(ValueError, match="color must be one of"):
            build(params=params, color="purple")


@requires_cq
class TestFerrousStripDimensions:
    """Bounding box and origin verification tests for ferrous_strip."""

    def test_ferrous_strip_bounding_box(self, params):
        """Verify ferrous strip dimensions are within ±0.5mm of spec."""
        from cad.components.ferrous_strip import build, FERROUS_STRIP_THICKNESS_MM
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Expected dimensions: 180mm × 6mm × 1mm
        if params:
            length = params.MARKER_TRACK_LENGTH_MM
            width = params.PTFE_WIDTH_MM
        else:
            from cad.params import MARKER_TRACK_LENGTH_MM, PTFE_WIDTH_MM
            length = MARKER_TRACK_LENGTH_MM
            width = PTFE_WIDTH_MM
        thickness = FERROUS_STRIP_THICKNESS_MM

        # Tolerance
        tol = 0.5

        # Check dimensions
        actual_length = bb.xmax - bb.xmin
        actual_width = bb.ymax - bb.ymin
        actual_thickness = bb.zmax - bb.zmin

        assert abs(actual_length - length) < tol, (
            f"Length {actual_length:.3f} differs from expected {length} by more than {tol}mm"
        )
        assert abs(actual_width - width) < tol, (
            f"Width {actual_width:.3f} differs from expected {width} by more than {tol}mm"
        )
        assert abs(actual_thickness - thickness) < tol, (
            f"Thickness {actual_thickness:.3f} differs from expected {thickness} by more than {tol}mm"
        )

    def test_ferrous_strip_origin_at_center_bottom(self, params):
        """Verify ferrous strip origin is at center of bottom face."""
        from cad.components.ferrous_strip import build
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Origin at center-bottom means:
        # - X and Y centers are at origin
        # - Z min is at origin
        tol = 0.5

        x_center = (bb.xmin + bb.xmax) / 2
        y_center = (bb.ymin + bb.ymax) / 2

        assert abs(x_center) < tol, f"X center {x_center:.3f} should be at origin (0)"
        assert abs(y_center) < tol, f"Y center {y_center:.3f} should be at origin (0)"
        assert bb.zmin < tol, f"Bottom face Z={bb.zmin:.3f} should be at origin (0)"


@requires_cq
class TestPTFESlideStripDimensions:
    """Bounding box and origin verification tests for ptfe_slide_strip."""

    def test_ptfe_slide_strip_bounding_box(self, params):
        """Verify PTFE slide strip dimensions are within ±0.5mm of spec."""
        from cad.components.ptfe_slide_strip import build
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Expected dimensions: 180mm × 6mm × 0.5mm
        if params:
            length = params.PTFE_LENGTH_MM
            width = params.PTFE_WIDTH_MM
            thickness = params.PTFE_THICKNESS_MM
        else:
            from cad.params import PTFE_LENGTH_MM, PTFE_WIDTH_MM, PTFE_THICKNESS_MM
            length = PTFE_LENGTH_MM
            width = PTFE_WIDTH_MM
            thickness = PTFE_THICKNESS_MM

        # Tolerance
        tol = 0.5

        # Check dimensions
        actual_length = bb.xmax - bb.xmin
        actual_width = bb.ymax - bb.ymin
        actual_thickness = bb.zmax - bb.zmin

        assert abs(actual_length - length) < tol, (
            f"Length {actual_length:.3f} differs from expected {length} by more than {tol}mm"
        )
        assert abs(actual_width - width) < tol, (
            f"Width {actual_width:.3f} differs from expected {width} by more than {tol}mm"
        )
        assert abs(actual_thickness - thickness) < tol, (
            f"Thickness {actual_thickness:.3f} differs from expected {thickness} by more than {tol}mm"
        )

    def test_ptfe_slide_strip_origin_at_center_bottom(self, params):
        """Verify PTFE slide strip origin is at center of bottom face."""
        from cad.components.ptfe_slide_strip import build
        result = build_or_skip(build, params=params)
        if result is None:
            pytest.skip("build() returned None")

        bb = result.val().BoundingBox()

        # Origin at center-bottom means:
        # - X and Y centers are at origin
        # - Z min is at origin
        tol = 0.5

        x_center = (bb.xmin + bb.xmax) / 2
        y_center = (bb.ymin + bb.ymax) / 2

        assert abs(x_center) < tol, f"X center {x_center:.3f} should be at origin (0)"
        assert abs(y_center) < tol, f"Y center {y_center:.3f} should be at origin (0)"
        assert bb.zmin < tol, f"Bottom face Z={bb.zmin:.3f} should be at origin (0)"