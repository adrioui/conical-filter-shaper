"""
Seam Guide Fin — SS 301 half-hard spring steel, laser-cut + press-formed.

A thin sliding blade that provides a repeatable reference for the factory seam of a
pre-seamed cone paper. Serration teeth on the shank grip matching serrations in the
Shell R slot. Guide-position markings at 5/7.5/10/12.5/15 mm are etched, not modelled.

Origin: fin base (bottom of slot engagement zone) at (0,0,0), fin extends in +Z.
Process note: "DO NOT anneal after laser cut" — material must remain half-hard.
Material: params.FIN_MATERIAL
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:
    cq = None  # type: ignore

import cad.params as _default_params


def build(params=None):  # -> cq.Workplane
    """
    Build the Seam Guide Fin as a thin solid.

    V1 honesty notes:
        - The 3D model is a flat laser-cut blank reference.
        - Press-formed serration teeth are a manufacturing/process detail and are not
          modelled as solid geometry in this stage.
    """
    if params is None:
        params = _default_params

    if cq is None:
        raise RuntimeError("CadQuery is not installed.")

    return cq.Workplane("XY").box(
        params.FIN_THICKNESS_MM,
        params.FIN_WIDTH_MM,
        params.FIN_LENGTH_MM,
        centered=(True, True, False),
    )
