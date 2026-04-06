"""
PTFE Slide Strip — Universal Filter Ruler
==========================================
Optional low-friction liner for the T-slot rail, reducing stick-slip during
arm adjustment and improving feel at the angle scale.
  - Material: PTFE, 0.5mm thick
  - Installed in the T-slot rail undercut channel
  - Press-fit or adhesive-backed

Qty per assembly: 2 (one per rail/arm)
Spec ref: docs/design_spec.md § T-Slot Rails (PTFE Insert note)
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None):  # -> cq.Workplane
    """Build PTFE slide strip solid. Not yet implemented."""
    raise NotImplementedError("ptfe_slide_strip.build() — Stage 2 implementation pending")
