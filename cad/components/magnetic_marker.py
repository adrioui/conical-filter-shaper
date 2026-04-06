"""
Magnetic Marker — Universal Filter Ruler
==========================================
Small repositionable angle-preset marker that snaps to the ferrous track strip.
  - Housing: Ø6mm × 4mm, 6061-T6 Al, color-anodized
  - Magnet: N52 neodymium, Ø5mm × 2mm, press-fit into housing
  - Pull force: ≥0.5 kg
  - Colors: Red, Blue, Green, Yellow (2 each = 8 total per set)

Spec ref: docs/design_spec.md § Magnetic Markers

Coordinate System
-----------------
- Origin: Center of bottom face (magnet face)
- X/Y: Horizontal plane
- Z: Up (top face at +Z)
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

from cad.params import (
    MARKER_DIAMETER_MM,
    MARKER_HEIGHT_MM,
    MARKER_MAGNET_DIAMETER_MM,
    MARKER_MAGNET_THICKNESS_MM,
)


# Marker geometry constants
MARKER_DOME_HEIGHT_MM = 1.0            # Height of the dome top for grip
MARKER_POCKET_CLEARANCE_MM = 0.1       # Small clearance for magnet press-fit


def build(params=None, color: str = "red") -> "cq.Workplane":
    """
    Build one magnetic marker housing solid.

    Parameters
    ----------
    params : module, optional
        The cad.params module (for consistent parameter access). If None,
        constants are imported directly.
    color : str
        Marker color for reference (geometry is same for all colors).
        Options: "red", "blue", "green", "yellow"

    Returns
    -------
    cq.Workplane
        A CadQuery workplane containing the magnetic marker housing solid.

    Geometry
    --------
    - Cylindrical housing: Ø6mm × 4mm
    - Magnet pocket: Ø5mm × 2mm deep on bottom face
    - Dome top: Rounded top surface for grip
    - Origin at center of bottom face
    """
    if cq is None:
        raise ImportError("CadQuery is required for magnetic_marker.build()")

    # Use params if provided, otherwise use imported constants
    if params is not None:
        diameter = params.MARKER_DIAMETER_MM
        height = params.MARKER_HEIGHT_MM
        magnet_diameter = params.MARKER_MAGNET_DIAMETER_MM
        magnet_thickness = params.MARKER_MAGNET_THICKNESS_MM
    else:
        diameter = MARKER_DIAMETER_MM
        height = MARKER_HEIGHT_MM
        magnet_diameter = MARKER_MAGNET_DIAMETER_MM
        magnet_thickness = MARKER_MAGNET_THICKNESS_MM

    valid_colors = {"red", "blue", "green", "yellow"}
    if color.lower() not in valid_colors:
        raise ValueError(f"color must be one of {valid_colors}, got {color!r}")

    # ── Main cylindrical body ─────────────────────────────────────────────────
    # Cylinder with origin at center-bottom

    radius = diameter / 2
    body_height = height - magnet_thickness  # Above magnet pocket

    # Create main cylinder (tall enough for body + dome)
    marker = (
        cq.Workplane("XY")
        .circle(radius)
        .extrude(body_height)
    )

    # ── Dome top ─────────────────────────────────────────────────────────────
    # Spherical dome on top for grip
    # Use a boolean operation to create a rounded top

    dome_sphere_radius = radius + MARKER_DOME_HEIGHT_MM  # Sphere radius for desired dome height

    # Create dome by intersecting cylinder with sphere
    dome = (
        cq.Workplane("XY")
        .sphere(dome_sphere_radius)
        .translate((0, 0, body_height - dome_sphere_radius + MARKER_DOME_HEIGHT_MM))
    )

    # Alternative: use loft with circle profile for simple dome approximation
    # We'll use a simple revolve approach for the dome

    # Create dome profile and revolve
    dome_profile = (
        cq.Workplane("YZ")
        .moveTo(0, body_height)
        .lineTo(radius - 0.5, body_height)  # Small flat top section
        .threePointArc((radius, body_height + MARKER_DOME_HEIGHT_MM), (radius - 0.5, body_height + MARKER_DOME_HEIGHT_MM))
        .lineTo(0, body_height + MARKER_DOME_HEIGHT_MM)
        .close()
    )

    # Actually, let's use a simpler approach: fillet the top edge
    # First, add the dome height to the body

    marker_with_dome = (
        cq.Workplane("XY")
        .circle(radius)
        .extrude(height - magnet_thickness + MARKER_DOME_HEIGHT_MM)
    )

    # Attempt to fillet dome edges - but typically domes are better done via loft
    # Let's use a simple cylindrical body with a filleted top edge

    try:
        # Fillet the top edge to create a rounded dome feel
        marker_with_dome = (
            cq.Workplane("XY")
            .circle(radius)
            .extrude(body_height + MARKER_DOME_HEIGHT_MM)
        )
        marker_with_dome = marker_with_dome.edges(">Z").fillet(radius * 0.6)
    except Exception:
        # If fillet fails, just use plain cylinder
        marker_with_dome = (
            cq.Workplane("XY")
            .circle(radius)
            .extrude(body_height + MARKER_DOME_HEIGHT_MM)
        )

    # ── Magnet pocket ─────────────────────────────────────────────────────────
    # Pocket on bottom face for magnet insertion
    # Slightly undersized for press-fit

    magnet_radius = magnet_diameter / 2 - MARKER_POCKET_CLEARANCE_MM

    magnet_pocket = (
        cq.Workplane("XY")
        .circle(magnet_radius)
        .extrude(magnet_thickness + 0.5)  # Pocket slightly deeper for adhesive
        .translate((0, 0, 0))
    )

    # Cut the pocket from bottom
    marker_final = marker_with_dome.cut(magnet_pocket)

    try:
        # Fillet bottom edge slightly for comfort
        marker_final = marker_final.edges("<Z").fillet(0.3)
    except Exception:
        pass

    return marker_final


def build_assembly(params=None) -> "cq.Workplane":
    """
    Build marker assembly with housing and magnet pocket.

    Returns
    -------
    cq.Workplane
        The marker assembly.
    """
    if cq is None:
        raise ImportError("CadQuery is required for magnetic_marker.build_assembly()")

    return build(params=params)