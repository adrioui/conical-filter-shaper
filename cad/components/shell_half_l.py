"""
Half-Shell L — left half of the split-shell mandrel.

Origin: cone apex (hinge point) at (0, 0, 0), cone axis along +Z.
        Shell spans the −X half-plane (split plane = XZ plane).
Preset: geometry is parameterised by the ConePreset passed to build().
        Default: params.DEFAULT_PRESET.

Material: params.SHELL_MATERIAL
Process:  params.SHELL_PROCESS
Drawing ref: manufacturing/drawings/shell_half_l_r{rev}.pdf
"""
from __future__ import annotations

try:
    import cadquery as cq
except ImportError:  # allow import in test/script context without CQ
    cq = None  # type: ignore

import cad.params as _default_params
from cad.components._shell_common import build_half_shell


def build(params=None, preset=None):  # -> cq.Workplane
    """
    Build Half-Shell L as a CadQuery Workplane.

    Args:
        params: params module or compatible namespace. Defaults to cad.params.
        preset: ConePreset to use. Defaults to params.DEFAULT_PRESET.

    Returns:
        cq.Workplane — Half-Shell L solid, apex at origin, +Z up.

    Key dims (from params):
        Wall thickness: params.SHELL_WALL_THICKNESS_MM
        Base tab extension: params.SHELL_BASE_TAB_EXTENSION_MM
        Follower bore: params.SHELL_FOLLOWER_BORE_DIA_MM
        Seam chamfer: params.SHELL_SEAM_RELIEF_CHAMFER_MM

    Note: Shell L is the mirror of Shell R minus the fin slot.
    """
    if params is None:
        params = _default_params
    if preset is None:
        preset = params.DEFAULT_PRESET

    if cq is None:
        raise RuntimeError("CadQuery is not installed. Run: pip install cadquery")

    return build_half_shell(params=params, preset=preset, side="left", include_fin_slot=False)
