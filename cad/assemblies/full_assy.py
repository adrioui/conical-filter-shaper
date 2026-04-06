"""
Full Assembly — Universal Filter Ruler
========================================
Top-level assembly: base plate + two arm assemblies + magnetic markers.

Sub-assemblies:
  - arm_assy (×2, left and right)

Origin: base plate bottom face center at (0, 0, 0), +Z up.

Not yet implemented — Stage 2.
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Assembly
    """
    Build the full ruler assembly.
    Not yet implemented.
    """
    raise NotImplementedError("full_assy.build() — Stage 2 implementation pending")
