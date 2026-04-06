"""
Magnetic Marker — Universal Filter Ruler
==========================================
Small repositionable angle-preset marker that snaps to the ferrous track strip.
  - Housing: Ø6mm × 4mm, 6061-T6 Al, color-anodized
  - Magnet: N52 neodymium, Ø5mm × 2mm, press-fit into housing
  - Pull force: ≥0.5 kg
  - Colors: Red, Blue, Green, Yellow (2 each = 8 total per set)

Spec ref: docs/design_spec.md § Magnetic Markers
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None, color: str = "red"):  # -> cq.Workplane
    """Build one magnetic marker housing solid. Not yet implemented."""
    raise NotImplementedError("magnetic_marker.build() — Stage 2 implementation pending")
