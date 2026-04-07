"""
Component build tests — Universal Coffee Filter Ruler v3.0.

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


# ═══════════════════════════════════════════════════════════════════════════════
# RULER ARM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@requires_cq
class TestRulerArm:

    def test_ruler_arm_left_builds(self, params):
        """Test that ruler_arm.build() returns a valid Workplane for left side."""
        from cad.components.ruler_arm import build
        result = build_or_skip(build, params=params, side="left")
        assert result is not None, "build() returned None"
        # Check it's a Workplane object
        import cadquery as cq
        assert isinstance(result, cq.Workplane), "build() should return cq.Workplane"

    def test_ruler_arm_right_builds(self, params):
        """Test that ruler_arm.build() returns a valid Workplane for right side."""
        from cad.components.ruler_arm import build
        result = build_or_skip(build, params=params, side="right")
        assert result is not None, "build() returned None"
        # Check it's a Workplane object
        import cadquery as cq
        assert isinstance(result, cq.Workplane), "build() should return cq.Workplane"

    def test_ruler_arm_invalid_side_raises(self, params):
        """Test that invalid side parameter raises ValueError."""
        from cad.components.ruler_arm import build
        with pytest.raises(ValueError, match="side must be 'left' or 'right'"):
            build(params=params, side="invalid")

    def test_ruler_arm_dimensions(self, params):
        """Test that arm bounding box matches expected dimensions (~120 x ~65 x ~1.2)."""
        from cad.components.ruler_arm import build
        arm = build_or_skip(build, params=params, side="left")
        
        # Get bounding box using CQ's bounding box method
        bbox = arm.combine().vals()[0].BoundingBox()
        length = bbox.xmax - bbox.xmin
        width = bbox.ymax - bbox.ymin
        thickness = bbox.zmax - bbox.zmin
        
        # Check approximate dimensions
        assert 118 <= length <= 122, f"Length {length} not ~120mm"
        assert 63 <= width <= 67, f"Width {width} not ~65mm"  
        assert 1.0 <= thickness <= 1.4, f"Thickness {thickness} not ~1.2mm"


# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT HINGE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@requires_cq
class TestPivotHinge:

    def test_pivot_hinge_builds(self, params):
        """Test that pivot_hinge.build() returns a valid Workplane."""
        from cad.components.pivot_hinge import build
        result = build_or_skip(build, params=params)
        assert result is not None, "build() returned None"
        import cadquery as cq
        assert isinstance(result, cq.Workplane), "build() should return cq.Workplane"


# ═══════════════════════════════════════════════════════════════════════════════
# THUMB SCREW TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@requires_cq
class TestThumbScrew:

    def test_thumb_screw_builds(self, params):
        """Test that thumb_screw.build() returns a valid Workplane."""
        from cad.components.thumb_screw import build
        result = build_or_skip(build, params=params)
        assert result is not None, "build() returned None"
        import cadquery as cq
        assert isinstance(result, cq.Workplane), "build() should return cq.Workplane"
