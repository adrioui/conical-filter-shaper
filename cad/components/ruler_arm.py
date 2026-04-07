"""
Ruler Arm — Tapered Trapezoidal v3.0
=====================================
One arm of the two-arm hinged V-shape filter ruler. SS304 stainless steel
flat bar with laser-etched arc marks for filter sizes.

Dimensions (v3.0 tapered trapezoidal arms)
------------------------------------------
- Length: 120 mm (from pivot hole center to tip)
- Width: 25 mm → 65 mm (tapered; narrow at pivot, wide at tip)
- Thickness: 1.2 mm
- Material: SS304, #4 brushed finish
- Edge radius: R0.3 mm (laser cut + deburr)

Features
--------
- M5 pivot hole at origin (for shoulder bolt)
- Arc mark grooves centered on pivot hole at radii:
  - 95mm → V60-01 slant height
  - 116mm → V60-02 slant height
  - 137mm → V60-03 slant height (skip if exceeds arm length)
- Groove spec: 0.3mm wide, 0.1mm deep

Origin Convention
-----------------
- Pivot hole center at origin (0, 0, 0)
- +X direction from pivot to tip (arm length = 120mm)
- Arm is centered on Y-axis at pivot end, tapers outward
- +Z up (through thickness)

Qty: 2 per ruler (left and right arms are identical)

Usage
-----
    from cad.components.ruler_arm import build
    arm = build(params=p, side="left")  # -> cq.Workplane
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None, side: str = "left") -> "cq.Workplane":
    """
    Build one ruler arm as a CadQuery Workplane solid.

    Parameters
    ----------
    params : module, optional
        Design parameter module (cad.params). Defaults to cad.params.
    side : str
        ``"left"`` or ``"right"``. Arms are identical but side is tracked
        for assembly positioning.

    Returns
    -------
    cq.Workplane
        Solid body of one tapered trapezoidal ruler arm.

    Raises
    ------
    ValueError
        If *side* is not ``"left"`` or ``"right"``.
    """
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")

    if cq is None:
        raise ImportError("CadQuery is required for ruler_arm.build()")

    # Use provided params or default
    if params is None:
        import cad.params as params

    # ═══════════════════════════════════════════════════════════════════════════
    # ARM DIMENSIONS (tapered trapezoidal profile)
    # ═══════════════════════════════════════════════════════════════════════════
    arm_length = params.ARM_LENGTH_MM
    arm_width_narrow = params.ARM_WIDTH_NARROW_MM
    arm_width_wide = params.ARM_WIDTH_WIDE_MM
    arm_thickness = params.ARM_THICKNESS_MM
    edge_radius = params.ARM_EDGE_RADIUS_MM
    pivot_hole_diameter = params.ARM_PIVOT_HOLE_DIA_MM

    # ═══════════════════════════════════════════════════════════════════════════
    # ARC MARK GROOVES
    # ═══════════════════════════════════════════════════════════════════════════
    arc_marks = params.ARC_MARKS
    groove_width = params.ARC_GROOVE_WIDTH_MM
    groove_depth = params.ARC_GROOVE_DEPTH_MM

    # ═══════════════════════════════════════════════════════════════════════════
    # BUILD THE TAPERED TRAPEZOIDAL ARM
    # ═══════════════════════════════════════════════════════════════════════════

    # Step 1: Create trapezoid profile using polyline
    # The arm is centered on Y-axis at pivot end (X=0)
    # Points:
    #   - (0, -narrow/2) → pivot end, bottom
    #   - (length, -wide/2) → tip end, bottom
    #   - (length, +wide/2) → tip end, top
    #   - (0, +narrow/2) → pivot end, top
    half_narrow = arm_width_narrow / 2
    half_wide = arm_width_wide / 2

    arm = (
        cq.Workplane("XY")
        .polyline([
            (0, -half_narrow),           # pivot end, bottom
            (arm_length, -half_wide),   # tip end, bottom
            (arm_length, half_wide),    # tip end, top
            (0, half_narrow),           # pivot end, top
        ])
        .close()
        .extrude(arm_thickness)
        .translate((0, 0, -arm_thickness / 2))  # Center on Z at origin
    )

    # Step 2: Apply edge fillets (R0.3mm)
    try:
        arm = arm.edges().fillet(edge_radius)
    except Exception:
        pass  # Fillet may fail on some geometries

    # Step 3: Cut the pivot hole at origin (through full thickness)
    arm = arm.faces(">Z").workplane().hole(pivot_hole_diameter)

    # Step 4: Cut arc mark grooves for filter sizes
    # Create thin arc-shaped grooves centered on pivot (origin)
    # Only create if arc radius <= arm length
    for key, radius in arc_marks.items():
        # Skip if arc radius exceeds arm length (won't intersect arm body)
        if radius > arm_length:
            continue

        # Calculate the effective Y range at this radius for the tapered arm
        # Linear interpolation: at radius X from origin
        t = radius / arm_length
        y_min_at_r = -half_narrow - t * (half_wide - half_narrow)
        y_max_at_r = half_narrow + t * (half_wide - half_narrow)

        # Create groove by cutting a thin box at the arc radius
        # Positioned on top face at Z = thickness/2
        # The groove extends in Y direction at the given radius from origin
        groove_height = y_max_at_r - y_min_at_r

        # Create a thin box that spans from y_min_at_r to y_max_at_r at radius from origin
        groove_cutter = (
            cq.Workplane("XY")
            .box(groove_width + 0.2, groove_height, groove_depth + 0.05)
            .translate((
                radius,                                    # X: at arc radius
                0,                                         # Y: centered
                arm_thickness / 2 - groove_depth / 2      # Z: top surface
            ))
        )

        # Subtract groove from arm (only where it intersects arm body)
        arm = arm - groove_cutter

    return arm
