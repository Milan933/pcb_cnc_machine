"""Dependency-light Phase 3 motion-system calculations.

The equations in this module are screening calculations. They are deliberately
separate from vendor selection and do not claim measured positioning accuracy,
motor torque at speed, screw straightness, or guide stiffness in a printed
assembly.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from cad.parameters import (
    PHASE3_MOTION_PARAMETERS,
    Phase3AxisParameters,
    Phase3MotionParameters,
    RailClassParameters,
)


@dataclass(frozen=True)
class ScrewScreen:
    """Resolution, torque, and whip screen for one axis."""

    axis: str
    lead_mm: float
    full_step_increment_mm: float
    microstep_increment_mm: float
    steps_per_mm: float
    design_force_n: float
    estimated_input_torque_nm: float
    unsupported_length_mm: float
    estimated_critical_speed_rpm: float
    screened_max_speed_rpm: float
    screened_max_feed_mm_min: float
    commissioning_feed_mm_min: float


@dataclass(frozen=True)
class AxisMotionScreen:
    """Combined axis layout result used by the report and tests."""

    axis: str
    travel_mm: float
    rail_class: str
    rail_count: int
    carriages_per_rail: int
    rail_center_spacing_mm: float
    guide_moment_reaction_n: float
    racking_moment_reaction_n: float
    screw: ScrewScreen


@dataclass(frozen=True)
class Phase3MotionScreen:
    """Full calculation output for the preliminary motion architecture."""

    axes: tuple[AxisMotionScreen, ...]
    pcb_edge_margin_mm: tuple[float, float]
    bed_area_margin_ok: bool
    moving_bed_mass_kg: float
    motor_torque_margin_xy: float
    motor_torque_margin_z: float
    recommended_microsteps: int


def steps_per_mm(
    lead_mm: float,
    microsteps: int,
    motor_steps_per_revolution: int = 200,
) -> float:
    """Return commanded steps per millimetre for a lead screw."""

    if lead_mm <= 0 or microsteps <= 0 or motor_steps_per_revolution <= 0:
        raise ValueError("lead, microsteps, and motor steps must be positive")
    return motor_steps_per_revolution * microsteps / lead_mm


def command_increment_mm(
    lead_mm: float,
    microsteps: int,
    motor_steps_per_revolution: int = 200,
) -> float:
    """Return the nominal controller command increment, not accuracy."""

    return 1.0 / steps_per_mm(lead_mm, microsteps, motor_steps_per_revolution)


def screw_input_torque_nm(
    axial_force_n: float,
    lead_mm: float,
    efficiency: float,
) -> float:
    """Estimate screw input torque from axial load and lead.

    This is a static screening equation. It omits starting friction, nut
    preload, acceleration, misalignment, and the motor torque-speed curve.
    """

    if axial_force_n < 0 or lead_mm <= 0 or not 0 < efficiency <= 1:
        raise ValueError("force, lead, and efficiency are out of range")
    return axial_force_n * lead_mm / (2.0 * math.pi * efficiency * 1000.0)


def screw_critical_speed_rpm(
    unsupported_length_mm: float,
    root_diameter_mm: float,
    youngs_modulus_n_per_mm2: float,
    density_kg_per_mm3: float,
) -> float:
    """Estimate pinned-pinned Euler screw critical speed.

    For a uniform round shaft, ``I/A = d²/16``. Real end conditions, screw
    straightness, bearing fits, nut drag, and the rotating assembly can lower
    the usable speed substantially; the result is therefore only a screen.
    """

    if unsupported_length_mm <= 0 or root_diameter_mm <= 0:
        raise ValueError("length and root diameter must be positive")
    if youngs_modulus_n_per_mm2 <= 0 or density_kg_per_mm3 <= 0:
        raise ValueError("material properties must be positive")
    area_ratio = root_diameter_mm**2 / 16.0
    natural_frequency_hz = (
        math.pi
        / (2.0 * unsupported_length_mm**2)
        * math.sqrt(youngs_modulus_n_per_mm2 * area_ratio / density_kg_per_mm3)
    )
    return 60.0 * natural_frequency_hz


def guide_force_from_moment(moment_nmm: float, spacing_mm: float) -> float:
    """Return the ideal differential guide reaction for a moment couple."""

    if moment_nmm < 0 or spacing_mm <= 0:
        raise ValueError("moment must be non-negative and spacing positive")
    return moment_nmm / spacing_mm


def rail_class_lookup(
    rail_class: str,
    candidates: tuple[RailClassParameters, ...] = PHASE3_MOTION_PARAMETERS.rail_classes,
) -> RailClassParameters:
    """Resolve a compact class name such as ``MGN12H``."""

    if len(rail_class) < 2:
        raise ValueError("rail_class must include family and block type")
    family, block_type = rail_class[:-1], rail_class[-1]
    for candidate in candidates:
        if candidate.family == family and candidate.block_type == block_type:
            return candidate
    raise KeyError(f"Unknown rail class: {rail_class}")


def _axis_screen(
    axis: Phase3AxisParameters,
    parameters: Phase3MotionParameters,
) -> AxisMotionScreen:
    moment_nmm = parameters.tool_point_test_load_n * parameters.tool_point_overhang_mm
    racking_moment_nmm = parameters.tool_point_test_load_n * 100.0
    screw = ScrewScreen(
        axis=axis.axis,
        lead_mm=axis.screw_lead_mm,
        full_step_increment_mm=command_increment_mm(
            axis.screw_lead_mm,
            1,
            parameters.motor_steps_per_revolution,
        ),
        microstep_increment_mm=command_increment_mm(
            axis.screw_lead_mm,
            parameters.recommended_microsteps,
            parameters.motor_steps_per_revolution,
        ),
        steps_per_mm=steps_per_mm(
            axis.screw_lead_mm,
            parameters.recommended_microsteps,
            parameters.motor_steps_per_revolution,
        ),
        design_force_n=axis.screw_design_force_n,
        estimated_input_torque_nm=screw_input_torque_nm(
            axis.screw_design_force_n,
            axis.screw_lead_mm,
            parameters.screw_efficiency,
        ),
        unsupported_length_mm=axis.screw_unsupported_length_mm,
        estimated_critical_speed_rpm=screw_critical_speed_rpm(
            axis.screw_unsupported_length_mm,
            parameters.screw_root_diameter_mm,
            parameters.screw_youngs_modulus_n_per_mm2,
            parameters.screw_density_kg_per_mm3,
        ),
        screened_max_speed_rpm=(
            parameters.critical_speed_margin
            * screw_critical_speed_rpm(
                axis.screw_unsupported_length_mm,
                parameters.screw_root_diameter_mm,
                parameters.screw_youngs_modulus_n_per_mm2,
                parameters.screw_density_kg_per_mm3,
            )
        ),
        screened_max_feed_mm_min=(
            parameters.critical_speed_margin
            * screw_critical_speed_rpm(
                axis.screw_unsupported_length_mm,
                parameters.screw_root_diameter_mm,
                parameters.screw_youngs_modulus_n_per_mm2,
                parameters.screw_density_kg_per_mm3,
            )
            * axis.screw_lead_mm
        ),
        commissioning_feed_mm_min=axis.commissioning_feed_mm_min,
    )
    return AxisMotionScreen(
        axis=axis.axis,
        travel_mm=axis.travel_mm,
        rail_class=axis.rail_class,
        rail_count=axis.rail_count,
        carriages_per_rail=axis.carriages_per_rail,
        rail_center_spacing_mm=axis.rail_center_spacing_mm,
        guide_moment_reaction_n=guide_force_from_moment(
            moment_nmm,
            axis.rail_center_spacing_mm,
        ),
        racking_moment_reaction_n=guide_force_from_moment(
            racking_moment_nmm,
            axis.rail_center_spacing_mm,
        ),
        screw=screw,
    )


def phase3_motion_screen(
    parameters: Phase3MotionParameters = PHASE3_MOTION_PARAMETERS,
) -> Phase3MotionScreen:
    """Calculate the preliminary axis screens from centralized parameters."""

    pcb_x, pcb_y = parameters.working_area_mm
    bed_x, bed_y, _ = parameters.moving_bed_support_mm
    margin_x = (bed_x - pcb_x) / 2.0
    margin_y = (bed_y - pcb_y) / 2.0
    axes = tuple(_axis_screen(axis, parameters) for axis in parameters.axes)
    xy_torque = max(
        item.screw.estimated_input_torque_nm
        for item in axes
        if item.axis in {"X", "Y"}
    )
    z_torque = next(item.screw.estimated_input_torque_nm for item in axes if item.axis == "Z")
    return Phase3MotionScreen(
        axes=axes,
        pcb_edge_margin_mm=(margin_x, margin_y),
        bed_area_margin_ok=(margin_x >= parameters.pcb_edge_margin_mm[0] and margin_y >= parameters.pcb_edge_margin_mm[1]),
        moving_bed_mass_kg=parameters.nominal_moving_bed_mass_kg,
        motor_torque_margin_xy=parameters.minimum_xy_holding_torque_nm / xy_torque,
        motor_torque_margin_z=parameters.minimum_z_holding_torque_nm / z_torque,
        recommended_microsteps=parameters.recommended_microsteps,
    )


def axis_by_name(
    axis_name: str,
    parameters: Phase3MotionParameters = PHASE3_MOTION_PARAMETERS,
) -> Phase3AxisParameters:
    """Return one centralized axis record."""

    for axis in parameters.axes:
        if axis.axis == axis_name.upper():
            return axis
    raise KeyError(f"Unknown axis: {axis_name}")
