"""Central project parameters for the foundation stage.

This module contains planning inputs only. It does not define machine-part
geometry and it does not claim that preliminary targets are final dimensions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ParameterStatus(str, Enum):
    """Evidence status used for controlled project values."""

    KNOWN = "known requirement"
    ASSUMPTION = "assumption"
    PRELIMINARY = "preliminary choice"
    CALCULATED = "calculated value"
    VERIFIED = "experimentally verified value"


@dataclass(frozen=True)
class RangeMm:
    """Inclusive planning range in millimetres."""

    minimum: float
    maximum: float

    def is_ordered(self) -> bool:
        return self.minimum <= self.maximum


@dataclass(frozen=True)
class ProjectParameters:
    """Centralized values currently known for the project foundation."""

    # User-provided preliminary working-envelope targets.
    target_x_travel_mm: float
    target_y_travel_mm: float
    target_z_travel_mm: RangeMm

    # User-provided approximate printer capability. Usable margins still need
    # to be measured and are not inferred here.
    voron_build_volume_mm: tuple[float, float, float]

    # User-provided project constraints and owned hardware.
    frame_material: str
    frame_is_predominantly_printed: bool
    owned_hardware: tuple[str, ...]

    # Direction convention is selected; physical origin placement remains open.
    coordinate_convention: tuple[str, str, str]
    machine_origin_status: str


INITIAL_PARAMETERS = ProjectParameters(
    target_x_travel_mm=200.0,
    target_y_travel_mm=150.0,
    target_z_travel_mm=RangeMm(minimum=30.0, maximum=50.0),
    voron_build_volume_mm=(350.0, 350.0, 350.0),
    frame_material="PETG",
    frame_is_predominantly_printed=True,
    owned_hardware=(
        "multiple NEMA 17 stepper motors",
        "Arduino CNC Shield / GRBL-compatible controller hardware",
        "Voron 2.4 350 printer",
    ),
    coordinate_convention=(
        "X: left to right, positive right",
        "Y: front to back, positive rear",
        "Z: down to up, positive upward",
    ),
    machine_origin_status="unresolved; select with the architecture datum",
)
