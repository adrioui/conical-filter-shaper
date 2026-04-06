"""
Arm Assembly — Universal Filter Ruler
=======================================
One sliding arm with its cam lock installed and positioned on the base plate rail.

Sub-components:
  - sliding_arm  (the aluminum arm body)
  - cam_lock     (eccentric cam + lever)

Origin: T-slot pivot center at (0, 0, 0), +Z up (arm sits above base plate top face).
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None, side: str = "left"):  # -> cq.Assembly
    """
    Build one arm assembly (sliding arm + cam lock).

    Parameters
    ----------
    params : module, optional
        Design parameter module. Defaults to cad.params.
    side : str
        "left" or "right" — determines mirroring of arm about center-line.

    Not yet implemented.
    """
    raise NotImplementedError("arm_assy.build() — Stage 2 implementation pending")
