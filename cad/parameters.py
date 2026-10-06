"""Central project parameters for the requirements and architecture stages.

This module contains controlled planning inputs only. The Phase 2 values are
parametric skeleton inputs and do not define detailed printable parts or
claim that preliminary targets are final dimensions.
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


@dataclass(frozen=True)
class Phase2SkeletonParameters:
    """Preliminary dimensions for the architecture-only CAD skeleton.

    These values describe envelopes, centerlines, and clearance assumptions.
    They are deliberately not printable-part dimensions and remain subject to
    the Phase 2 review and later motion, BOM, and structural evidence.
    """

    # The owner accepted the B working-area baseline; tool travel is a
    # separate preliminary packaging assumption with 10 mm nominal access on
    # each working-area edge.
    working_area_mm: tuple[float, float]
    tool_travel_mm: tuple[float, float, float]
    travel_margin_each_end_mm: float

    # Envelope-only bed and base references, with the workholding reference
    # plane at Z=0 and positive Z upward.
    bed_envelope_mm: tuple[float, float, float]
    base_envelope_mm: tuple[float, float, float]
    workholding_reference_z_mm: float

    # Gantry screening bounds. A closed or ribbed monocoque is evaluated at
    # this section depth; no wall, rib, or fastener geometry is implied.
    gantry_clear_span_mm: float
    gantry_outer_width_mm: float
    gantry_section_depth_mm: float
    gantry_section_height_mm: float
    gantry_crossbeam_bottom_z_mm: float
    overall_envelope_mm: tuple[float, float, float]

    # Reference spacing for guide and screw interfaces, not selected hardware.
    y_rail_center_spacing_mm: float
    x_rail_vertical_spacing_mm: float
    z_rail_center_spacing_mm: float
    z_carriage_envelope_mm: tuple[float, float, float]
    rail_end_margin_mm: float
    screw_end_margin_mm: float

    # Hardware envelopes remain deliberately generic until the motion phase.
    spindle_envelope_diameter_mm: float
    spindle_envelope_length_mm: float
    tool_stickout_mm: float
    tool_point_overhang_mm: float
    reference_axis_diameter_mm: float
    reference_screw_diameter_mm: float

    # The print-volume limits are inherited rather than silently redefined.
    preferred_printed_dimension_mm: float
    conditional_printed_dimension_mm: float


PHASE2_SKELETON_PARAMETERS = Phase2SkeletonParameters(
    working_area_mm=(200.0, 150.0),
    tool_travel_mm=(220.0, 170.0, 40.0),
    travel_margin_each_end_mm=10.0,
    bed_envelope_mm=(240.0, 190.0, 12.0),
    base_envelope_mm=(320.0, 280.0, 28.0),
    workholding_reference_z_mm=0.0,
    gantry_clear_span_mm=280.0,
    gantry_outer_width_mm=320.0,
    gantry_section_depth_mm=60.0,
    gantry_section_height_mm=60.0,
    gantry_crossbeam_bottom_z_mm=110.0,
    # The machine-level skeleton includes reference screw end margins; this
    # is a packaging envelope, not a one-piece printable-part limit.
    overall_envelope_mm=(340.0, 290.0, 220.0),
    y_rail_center_spacing_mm=220.0,
    x_rail_vertical_spacing_mm=50.0,
    z_rail_center_spacing_mm=60.0,
    z_carriage_envelope_mm=(90.0, 40.0, 70.0),
    rail_end_margin_mm=30.0,
    screw_end_margin_mm=30.0,
    spindle_envelope_diameter_mm=52.0,
    spindle_envelope_length_mm=120.0,
    tool_stickout_mm=15.0,
    tool_point_overhang_mm=50.0,
    reference_axis_diameter_mm=2.0,
    reference_screw_diameter_mm=4.0,
    preferred_printed_dimension_mm=320.0,
    conditional_printed_dimension_mm=330.0,
)


@dataclass(frozen=True)
class Phase2AParameters:
    """Controlled assumptions for the focused A-versus-B structural study.

    These are equivalent-section, mass, and manufacturing estimates used to
    make the comparison reproducible. They are not measured PETG properties,
    supplier data, or detailed part dimensions.
    """

    test_load_n: float
    tool_point_deflection_target_mm: float
    tool_point_deflection_acceptance_mm: float
    tool_point_overhang_mm: float
    effective_petg_modulus_n_per_mm2: float
    effective_petg_poisson_ratio: float
    torsion_half_span_mm: float
    racking_force_offset_mm: float
    racking_tool_arm_mm: float
    y_guide_spacing_mm: float
    nominal_y_acceleration_m_per_s2: float
    guide_friction_coefficient: float
    screw_efficiency: float
    screw_leads_mm: tuple[float, ...]

    # Architecture A: an aggressively deep stationary integrated gantry.
    a_section_width_mm: float
    a_section_depth_mm: float
    a_section_wall_mm: float
    a_beam_bottom_z_mm: float
    a_moving_bed_support_thickness_mm: float
    a_support_bending_length_mm: float
    a_support_effective_second_moment_mm4: float
    a_z_effective_stiffness_n_per_mm: float
    a_joint_effective_stiffness_n_per_mm: float
    a_racking_rotational_stiffness_nmm_per_rad: float

    # Architecture B: a lighter moving gantry with explicit side interfaces.
    b_section_width_mm: float
    b_section_depth_mm: float
    b_section_wall_mm: float
    b_support_bending_length_mm: float
    b_support_effective_second_moment_mm4: float
    b_z_effective_stiffness_n_per_mm: float
    b_joint_effective_stiffness_n_per_mm: float
    b_racking_rotational_stiffness_nmm_per_rad: float

    # Moving-mass breakdowns. The values are nominal estimates with ranges in
    # the Phase 2A report; no item is a purchased-part fact.
    a_moving_mass_items_kg: tuple[tuple[str, float], ...]
    b_moving_mass_items_kg: tuple[tuple[str, float], ...]
    a_printed_mass_items_kg: tuple[tuple[str, float], ...]
    b_printed_mass_items_kg: tuple[tuple[str, float], ...]

    # Manufacturing comparison estimates for the optimized skeleton concepts.
    a_print_hours_range: tuple[float, float]
    b_print_hours_range: tuple[float, float]
    a_structural_print_count: int
    b_structural_print_count: int
    a_largest_print_mm: tuple[float, float, float]
    b_largest_print_mm: tuple[float, float, float]
    a_structural_joint_count: int
    b_structural_joint_count: int
    a_heat_set_insert_count: int
    b_heat_set_insert_count: int
    a_through_bolt_count: int
    b_through_bolt_count: int
    a_rail_seat_count: int
    b_rail_seat_count: int
    a_cable_drag_n: float
    b_cable_drag_n: float


PHASE2A_PARAMETERS = Phase2AParameters(
    test_load_n=5.0,
    tool_point_deflection_target_mm=0.020,
    tool_point_deflection_acceptance_mm=0.030,
    tool_point_overhang_mm=50.0,
    effective_petg_modulus_n_per_mm2=2000.0,
    effective_petg_poisson_ratio=0.35,
    torsion_half_span_mm=140.0,
    racking_force_offset_mm=100.0,
    racking_tool_arm_mm=100.0,
    y_guide_spacing_mm=220.0,
    nominal_y_acceleration_m_per_s2=0.20,
    guide_friction_coefficient=0.15,
    screw_efficiency=0.35,
    screw_leads_mm=(2.0, 4.0),
    a_section_width_mm=90.0,
    a_section_depth_mm=100.0,
    a_section_wall_mm=4.0,
    a_beam_bottom_z_mm=80.0,
    a_moving_bed_support_thickness_mm=8.0,
    a_support_bending_length_mm=160.0,
    a_support_effective_second_moment_mm4=800000.0,
    a_z_effective_stiffness_n_per_mm=2000.0,
    a_joint_effective_stiffness_n_per_mm=1666.6666667,
    a_racking_rotational_stiffness_nmm_per_rad=20000000.0,
    b_section_width_mm=60.0,
    b_section_depth_mm=70.0,
    b_section_wall_mm=4.0,
    b_support_bending_length_mm=80.0,
    b_support_effective_second_moment_mm4=30000.0,
    b_z_effective_stiffness_n_per_mm=1428.5714286,
    b_joint_effective_stiffness_n_per_mm=625.0,
    b_racking_rotational_stiffness_nmm_per_rad=10000000.0,
    a_moving_mass_items_kg=(
        ("PCB", 0.09),
        ("spoilboard", 0.30),
        ("printed moving-bed support", 0.42),
        ("registration and workholding", 0.10),
        ("Y carriages, screw nut, and moving hardware", 0.28),
        ("cable and probe allowance", 0.05),
    ),
    b_moving_mass_items_kg=(
        ("deep printed gantry and side interfaces", 1.65),
        ("Y carriages, screw nut, and moving hardware", 0.35),
        ("X rails, carriage, and screw allowance", 0.40),
        ("Z guides, carriage, screw, and mount allowance", 0.55),
        ("spindle screening mass", 0.80),
        ("cables and probe allowance", 0.20),
    ),
    a_printed_mass_items_kg=(
        ("integrated fixed gantry and supports", 2.20),
        ("base and interface structure", 1.50),
        ("moving bed support", 0.42),
    ),
    b_printed_mass_items_kg=(
        ("fixed base and interface structure", 1.50),
        ("moving gantry and side interfaces", 1.65),
        ("fixed bed support", 0.30),
        ("service and probe structural allowance", 0.25),
    ),
    a_print_hours_range=(32.0, 42.0),
    b_print_hours_range=(28.0, 38.0),
    a_structural_print_count=5,
    b_structural_print_count=6,
    a_largest_print_mm=(320.0, 100.0, 220.0),
    b_largest_print_mm=(300.0, 80.0, 160.0),
    a_structural_joint_count=4,
    b_structural_joint_count=6,
    a_heat_set_insert_count=16,
    b_heat_set_insert_count=24,
    a_through_bolt_count=12,
    b_through_bolt_count=20,
    a_rail_seat_count=4,
    b_rail_seat_count=6,
    a_cable_drag_n=0.50,
    b_cable_drag_n=1.00,
)
