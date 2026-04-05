"""
Reference dripper cone dimensions for assembly fit-check tests.
Used to verify the mandrel will fit inside each target dripper without clash.
Sources: manufacturer spec sheets + community measurements (see refs/dripper_dimensions/).
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DripperProfile:
    name: str
    included_angle_deg: float       # Full cone angle of dripper interior
    inner_diameter_at_rim_mm: float # Dripper opening diameter
    depth_mm: float                 # Interior cone depth
    target_preset_label: str        # Which ConePreset targets this dripper


DRIPPER_PROFILES: list[DripperProfile] = [
    DripperProfile(
        name="Hario V60 #2",
        included_angle_deg=60.0,
        inner_diameter_at_rim_mm=90.0,
        depth_mm=78.0,
        target_preset_label="P2",
    ),
    DripperProfile(
        name="Timemore B75",
        included_angle_deg=48.0,
        inner_diameter_at_rim_mm=75.0,
        depth_mm=70.0,
        target_preset_label="P1",
    ),
    DripperProfile(
        name="UFO Dripper",
        included_angle_deg=80.0,
        inner_diameter_at_rim_mm=110.0,
        depth_mm=58.0,
        target_preset_label="P3",
    ),
    DripperProfile(
        name="Origami Narrow",
        included_angle_deg=48.0,
        inner_diameter_at_rim_mm=72.0,
        depth_mm=68.0,
        target_preset_label="P1",
    ),
]
