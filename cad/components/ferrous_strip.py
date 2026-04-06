"""
Ferrous Track Strip — Universal Filter Ruler
==============================================
Mild steel strip recessed into the base plate top surface;
provides the magnetic attraction surface for the magnetic markers.
  - Dimensions: 180mm × 6mm × 1mm
  - Material: Mild steel, zinc plated
  - Recess depth into base plate: 1mm
  - Adhesive-mounted (or press-fit in recess)

Qty per assembly: 1
Spec ref: docs/design_spec.md § Magnetic Track
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None):  # -> cq.Workplane
    """Build ferrous strip solid. Not yet implemented."""
    raise NotImplementedError("ferrous_strip.build() — Stage 2 implementation pending")
