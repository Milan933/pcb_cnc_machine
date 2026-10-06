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
class NumericRange:
    """Unit-bearing range whose unit is documented at the field site."""

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


@dataclass(frozen=True)
class WorkingAreaOption:
    """PCB working-area option used by the Phase 1 packaging trade study."""

    option_id: str
    pcb_x_mm: float
    pcb_y_mm: float


@dataclass(frozen=True)
class ZErrorAllocation:
    """Initial Z error allocation; values are not measured machine results."""

    name: str
    allocation_mm: float
    compensatable: bool
    notes: str


@dataclass(frozen=True)
class Phase1Requirements:
    """Quantitative Phase 1 screening requirements and test targets."""

    # Process stock and tool candidates.
    nominal_copper_thickness_mm: float
    copper_thickness_mm: RangeMm
    pcb_thickness_mm: RangeMm
    isolation_depth_mm: RangeMm
    initial_isolation_depth_mm: float
    v_bit_included_angles_deg: tuple[float, ...]
    v_bit_tip_diameter_mm: RangeMm
    fine_end_mill_diameter_mm: RangeMm
    outline_end_mill_diameter_mm: float
    drill_diameter_mm: RangeMm

    # These are starting CAM windows, not machine capability claims.
    isolation_feed_mm_min: NumericRange
    drilling_feed_mm_min: NumericRange
    outline_feed_mm_min: NumericRange
    spindle_speed_rpm: NumericRange
    initial_spindle_speed_rpm: float

    # Spindle screening envelope; no spindle is selected.
    spindle_power_w: NumericRange
    spindle_mass_kg: NumericRange
    spindle_diameter_classes_mm: tuple[float, ...]
    er11_tooling_required: bool
    spindle_runout_target_mm: float
    spindle_runout_acceptance_max_mm: float

    # Motion and tool-point screening targets.
    tool_point_deflection_target_mm: float
    tool_point_deflection_test_load_n: float
    xy_absolute_error_target_mm: float
    xy_absolute_error_acceptance_mm: float
    xy_repeatability_target_mm: float
    xy_repeatability_acceptance_mm: float
    xy_backlash_target_mm: float
    xy_backlash_acceptance_mm: float
    xy_straightness_target_mm: float
    xy_straightness_acceptance_mm: float
    xy_squareness_target_mm_per_100mm: float
    xy_squareness_acceptance_mm_per_100mm: float

    # Z and probing targets.
    z_machine_error_budget_mm: float
    z_map_residual_target_mm: float
    z_map_residual_acceptance_mm: float
    height_map_grid_max_spacing_mm: float
    height_map_refinement_spacing_mm: float

    # PETG printability screening limits.
    preferred_printed_dimension_mm: float
    conditional_printed_dimension_mm: float
    xy_packaging_allowance_total_mm: NumericRange

    working_area_options: tuple[WorkingAreaOption, ...]
    recommended_working_area_option_id: str
    z_error_budget: tuple[ZErrorAllocation, ...]


PHASE1_REQUIREMENTS = Phase1Requirements(
    nominal_copper_thickness_mm=0.035,
    copper_thickness_mm=RangeMm(minimum=0.0175, maximum=0.070),
    pcb_thickness_mm=RangeMm(minimum=0.8, maximum=2.0),
    isolation_depth_mm=RangeMm(minimum=0.05, maximum=0.15),
    initial_isolation_depth_mm=0.10,
    v_bit_included_angles_deg=(30.0, 60.0),
    v_bit_tip_diameter_mm=RangeMm(minimum=0.0762, maximum=0.1270),
    fine_end_mill_diameter_mm=RangeMm(minimum=0.20, maximum=0.40),
    outline_end_mill_diameter_mm=0.79375,
    drill_diameter_mm=RangeMm(minimum=0.30, maximum=1.00),
    isolation_feed_mm_min=NumericRange(minimum=100.0, maximum=600.0),
    drilling_feed_mm_min=NumericRange(minimum=30.0, maximum=200.0),
    outline_feed_mm_min=NumericRange(minimum=100.0, maximum=800.0),
    spindle_speed_rpm=NumericRange(minimum=10000.0, maximum=30000.0),
    initial_spindle_speed_rpm=20000.0,
    spindle_power_w=NumericRange(minimum=50.0, maximum=150.0),
    spindle_mass_kg=NumericRange(minimum=0.30, maximum=0.80),
    spindle_diameter_classes_mm=(25.0, 40.0, 52.0),
    er11_tooling_required=True,
    spindle_runout_target_mm=0.010,
    spindle_runout_acceptance_max_mm=0.020,
    tool_point_deflection_target_mm=0.020,
    tool_point_deflection_test_load_n=5.0,
    xy_absolute_error_target_mm=0.050,
    xy_absolute_error_acceptance_mm=0.100,
    xy_repeatability_target_mm=0.030,
    xy_repeatability_acceptance_mm=0.050,
    xy_backlash_target_mm=0.030,
    xy_backlash_acceptance_mm=0.050,
    xy_straightness_target_mm=0.050,
    xy_straightness_acceptance_mm=0.100,
    xy_squareness_target_mm_per_100mm=0.050,
    xy_squareness_acceptance_mm_per_100mm=0.100,
    z_machine_error_budget_mm=0.040,
    z_map_residual_target_mm=0.020,
    z_map_residual_acceptance_mm=0.030,
    height_map_grid_max_spacing_mm=25.0,
    height_map_refinement_spacing_mm=12.5,
    preferred_printed_dimension_mm=320.0,
    conditional_printed_dimension_mm=330.0,
    xy_packaging_allowance_total_mm=NumericRange(minimum=60.0, maximum=100.0),
    working_area_options=(
        WorkingAreaOption("A_160x100", 160.0, 100.0),
        WorkingAreaOption("B_200x150", 200.0, 150.0),
        WorkingAreaOption("C_250x180", 250.0, 180.0),
    ),
    recommended_working_area_option_id="B_200x150",
    z_error_budget=(
        ZErrorAllocation(
            "machine structural deflection at process load",
            0.015,
            False,
            "Reduce through geometry and verify with a tool-point load test.",
        ),
        ZErrorAllocation(
            "linear-guide play or preload loss",
            0.005,
            False,
            "Require supported, preloaded guides and a repeatability test.",
        ),
        ZErrorAllocation(
            "lead-screw axial play and compliance",
            0.005,
            False,
            "Control by bearing arrangement and anti-backlash strategy.",
        ),
        ZErrorAllocation(
            "spindle, collet, and tool axial seating",
            0.005,
            False,
            "Measure with the actual tool and retention method.",
        ),
        ZErrorAllocation(
            "workholding distortion not captured by the map",
            0.005,
            False,
            "Use uniform support and verify after loading the board.",
        ),
        ZErrorAllocation(
            "thermal drift during one job",
            0.005,
            False,
            "Warm up consistently or re-probe when drift is observed.",
        ),
        ZErrorAllocation(
            "spoilboard and PCB surface variation covered by mapping",
            0.100,
            True,
            "Coverage allowance, not a residual error; map domain must include it.",
        ),
        ZErrorAllocation(
            "probe repeatability",
            0.010,
            True,
            "Measure repeated conductive probes with the actual circuit.",
        ),
        ZErrorAllocation(
            "height-map interpolation residual",
            0.010,
            True,
            "Compare grid spacings against independent check points.",
        ),
    ),
)


def non_compensatable_z_budget_mm(
    requirements: Phase1Requirements = PHASE1_REQUIREMENTS,
) -> float:
    """Return the sum of the initial non-compensatable Z allocations."""

    return sum(
        item.allocation_mm
        for item in requirements.z_error_budget
        if not item.compensatable
    )
