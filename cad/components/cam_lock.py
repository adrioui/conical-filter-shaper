"""
Cam Lock — Universal Filter Ruler
====================================
Eccentric cam mechanism that clamps the sliding arm in position.
  - 90° throw, single-handed operation
  - Cam body: SS 316, eccentric pivot
  - Lever: 6061-T6 Al, 25mm, knurled end
  - Mounting: M5 shoulder bolt into base plate
  - Clamping force: ≥50 N

Qty per assembly: 2 (one per arm)
Spec ref: docs/design_spec.md § Cam Lock Mechanism
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore


def build(params=None):  # -> cq.Workplane
    """Build cam lock body solid. Not yet implemented."""
    raise NotImplementedError("cam_lock.build() — Stage 2 implementation pending")
