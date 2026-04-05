"""
Dual-spiral cam track path generation.
Pure math — no CadQuery imports.

The cam ring has 6-fold alternating symmetry: 3 preset dwell arcs repeated 180° apart
(one set per follower pin). Each single follower path spans 180°; the second follower is
phase-shifted by 180° so the pair fills the full 360° ring.

Coordinates: (angle_deg, radius_mm) in polar form.
"""
from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass
class CamTrackPoint:
    angle_deg: float
    radius_mm: float


def sinusoidal_transition(
    start_radius: float,
    end_radius: float,
    n_points: int = 64,
) -> list[float]:
    """
    Generate radii for a sinusoidal (S-curve) transition between two dwell radii.
    Returns a list of n_points radius values from start_radius to end_radius.
    """
    radii = []
    for i in range(n_points):
        t = i / (n_points - 1)
        # Sinusoidal ease: 0.5 × (1 − cos(π × t))
        s = 0.5 * (1.0 - math.cos(math.pi * t))
        radii.append(start_radius + s * (end_radius - start_radius))
    return radii


def build_cam_track(
    dwell_radii: list[float],
    dwell_arc_deg: float,
    transition_arc_deg: float,
    n_transition_points: int = 64,
    offset_deg: float = 0.0,
) -> list[CamTrackPoint]:
    """
    Build one 180° cam track for a single follower pin.

    The track has `len(dwell_radii)` dwell segments interleaved with
    `len(dwell_radii)` sinusoidal transition segments.

    Args:
        dwell_radii:          List of dwell radii, one per preset [P1, P2, P3, …].
        dwell_arc_deg:        Angular span of each dwell arc.
        transition_arc_deg:   Angular span of each transition arc.
        n_transition_points:  Number of sample points per transition.
        offset_deg:           Starting angle offset (use 180° for second follower).

    Returns:
        List of (angle_deg, radius_mm) CamTrackPoints covering one 180° follower path.
    """
    n = len(dwell_radii)
    period_deg = dwell_arc_deg + transition_arc_deg
    assert abs(n * period_deg - 180.0) < 0.01, (
        f"Track does not close: {n} presets × {period_deg}° ≠ 180° per follower"
    )

    points: list[CamTrackPoint] = []
    current_angle = offset_deg

    for i in range(n):
        r_dwell = dwell_radii[i]
        r_next = dwell_radii[(i + 1) % n]

        # Dwell arc
        dwell_step = dwell_arc_deg / max(n_transition_points // 4, 4)
        a = current_angle
        while a < current_angle + dwell_arc_deg:
            points.append(CamTrackPoint(a % 360.0, r_dwell))
            a += dwell_step
        current_angle += dwell_arc_deg

        # Sinusoidal transition
        radii = sinusoidal_transition(r_dwell, r_next, n_transition_points)
        ang_step = transition_arc_deg / n_transition_points
        for j, r in enumerate(radii):
            points.append(CamTrackPoint((current_angle + j * ang_step) % 360.0, r))
        current_angle += transition_arc_deg

    return points


def cam_track_for_preset_radii(params) -> tuple[list[CamTrackPoint], list[CamTrackPoint]]:
    """
    Build cam tracks for both follower pins using params from cad.params.

    Returns:
        (follower_L_track, follower_R_track) — R track is L track offset by 180°.
    """
    dwell_radii = [p.cam_dwell_radius_mm for p in params.PRESETS]
    track_L = build_cam_track(
        dwell_radii=dwell_radii,
        dwell_arc_deg=params.CAM_DWELL_ARC_DEG,
        transition_arc_deg=params.CAM_TRANSITION_ARC_DEG,
        offset_deg=0.0,
    )
    track_R = build_cam_track(
        dwell_radii=dwell_radii,
        dwell_arc_deg=params.CAM_DWELL_ARC_DEG,
        transition_arc_deg=params.CAM_TRANSITION_ARC_DEG,
        offset_deg=180.0,
    )
    return track_L, track_R
