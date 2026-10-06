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
    preferred_printed_dimension_mm=300.0,
    conditional_printed_dimension_mm=320.0,
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

    # The owner accepted the B working-area option; tool travel is a
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
    preferred_printed_dimension_mm=300.0,
    conditional_printed_dimension_mm=320.0,
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


@dataclass(frozen=True)
class RailClassParameters:
    """Vendor-reference envelope for a rail class, not a purchase lock."""

    family: str
    block_type: str
    assembly_width_mm: float
    assembly_height_mm: float
    block_length_mm: float
    dynamic_load_kn: float
    static_load_kn: float
    rated_moment_mr_nm: float
    rated_moment_mp_nm: float
    rated_moment_my_nm: float
    block_mass_kg: float
    rail_mass_kg_per_m: float
    rail_mounting_bolt: str
    availability_class: str
    source_url: str


@dataclass(frozen=True)
class Phase3AxisParameters:
    """Preliminary axis-level motion layout and transmission inputs."""

    axis: str
    travel_mm: float
    rail_class: str
    rail_count: int
    carriages_per_rail: int
    rail_center_spacing_mm: float
    rail_length_mm: float
    screw_lead_mm: float
    screw_length_mm: float
    screw_unsupported_length_mm: float
    screw_design_force_n: float
    commissioning_feed_mm_min: float
    home_direction: str
    fixed_bearing_location: str
    floating_bearing_location: str


@dataclass(frozen=True)
class Phase3MotionParameters:
    """Central Phase 3 motion-system screening parameters.

    These values describe a review layout and component classes. Exact
    supplier, preload, rail lengths, motors, drivers, spindle, and printed
    interfaces remain open until measured hardware and physical evidence are
    available.
    """

    working_area_mm: tuple[float, float]
    screened_travel_mm: tuple[float, float, float]
    moving_bed_support_mm: tuple[float, float, float]
    spoilboard_envelope_mm: tuple[float, float, float]
    pcb_edge_margin_mm: tuple[float, float]
    nominal_moving_bed_mass_kg: float
    tool_point_test_load_n: float
    tool_point_overhang_mm: float
    rail_classes: tuple[RailClassParameters, ...]
    axes: tuple[Phase3AxisParameters, ...]
    screw_candidate_leads_mm: tuple[float, ...]
    screw_root_diameter_mm: float
    screw_youngs_modulus_n_per_mm2: float
    screw_density_kg_per_mm3: float
    screw_efficiency: float
    critical_speed_margin: float
    motor_steps_per_revolution: int
    recommended_microsteps: int
    motor_mounting_square_mm: float
    motor_body_length_range_mm: tuple[float, float]
    motor_shaft_diameter_mm: float
    motor_shaft_engagement_mm: float
    minimum_xy_holding_torque_nm: float
    minimum_z_holding_torque_nm: float
    motor_phase_current_screening_range_a: tuple[float, float]
    bearing_bore_mm: float
    fixed_bearing_strategy: str
    floating_bearing_strategy: str
    coupler_strategy: str
    nut_strategy_xy: str
    nut_strategy_z: str
    backlash_target_mm: float
    controller_family: str
    driver_candidates: tuple[str, ...]
    driver_microstep_limits: tuple[tuple[str, int], ...]
    controller_required_interfaces: tuple[str, ...]
    controller_identification_checklist: tuple[str, ...]
    home_positions: tuple[tuple[str, str], ...]
    machine_coordinate_definition: str
    work_coordinate_definition: str
    machine_envelope_mm: tuple[float, float, float]
    service_footprint_mm: tuple[float, float, float]
    rail_reference_envelopes_mm: tuple[tuple[str, tuple[float, float]], ...]
    reference_screw_diameter_mm: float
    reference_nut_envelope_mm: tuple[float, float, float]
    reference_motor_envelope_mm: tuple[float, float, float]
    reference_bearing_support_envelopes_mm: tuple[tuple[str, tuple[float, float, float]], ...]
    reference_lower_bearing_support_envelope_mm: tuple[float, float, float]
    reference_coupler_envelopes_mm: tuple[tuple[str, tuple[float, float, float]], ...]
    spindle_mount_envelope_mm: tuple[float, float, float]
    x_rail_center_y_mm: float
    x_rail_center_z_mm: float
    y_rail_center_z_mm: float
    z_rail_center_y_mm: float
    z_rail_base_z_mm: float
    z_screw_center_offset_y_mm: float
    y_carriage_center_offsets_mm: tuple[float, float]
    reference_end_clearance_mm: float
    reference_lower_support_overlap_mm: float
    reference_motor_clearance_mm: float
    spindle_mount_min_z_mm: float
    physical_motion_tests: tuple[str, ...]
    source_urls: tuple[str, ...]


PHASE3_RAIL_CLASSES = (
    RailClassParameters(
        family="MGN9",
        block_type="C",
        assembly_width_mm=20.0,
        assembly_height_mm=10.0,
        block_length_mm=30.0,
        dynamic_load_kn=2.01,
        static_load_kn=2.84,
        rated_moment_mr_nm=13.05,
        rated_moment_mp_nm=8.97,
        rated_moment_my_nm=8.97,
        block_mass_kg=0.012,
        rail_mass_kg_per_m=0.38,
        rail_mounting_bolt="M3x8",
        availability_class="low-cost / widely available; clone variation requires inspection",
        source_url="https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf",
    ),
    RailClassParameters(
        family="MGN9",
        block_type="H",
        assembly_width_mm=20.0,
        assembly_height_mm=10.0,
        block_length_mm=39.9,
        dynamic_load_kn=2.50,
        static_load_kn=3.93,
        rated_moment_mr_nm=19.71,
        rated_moment_mp_nm=21.47,
        rated_moment_my_nm=21.47,
        block_mass_kg=0.020,
        rail_mass_kg_per_m=0.38,
        rail_mounting_bolt="M3x8",
        availability_class="low-cost / widely available; clone variation requires inspection",
        source_url="https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf",
    ),
    RailClassParameters(
        family="MGN12",
        block_type="C",
        assembly_width_mm=27.0,
        assembly_height_mm=13.0,
        block_length_mm=35.0,
        dynamic_load_kn=2.84,
        static_load_kn=3.92,
        rated_moment_mr_nm=25.48,
        rated_moment_mp_nm=13.72,
        rated_moment_my_nm=13.72,
        block_mass_kg=0.025,
        rail_mass_kg_per_m=0.65,
        rail_mounting_bolt="M3x8",
        availability_class="medium-cost / widely available; clone variation requires inspection",
        source_url="https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf",
    ),
    RailClassParameters(
        family="MGN12",
        block_type="H",
        assembly_width_mm=27.0,
        assembly_height_mm=13.0,
        block_length_mm=47.6,
        dynamic_load_kn=4.27,
        static_load_kn=5.90,
        rated_moment_mr_nm=38.40,
        rated_moment_mp_nm=37.49,
        rated_moment_my_nm=37.49,
        block_mass_kg=0.047,
        rail_mass_kg_per_m=0.65,
        rail_mounting_bolt="M3x8",
        availability_class="medium-cost / widely available; clone variation requires inspection",
        source_url="https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf",
    ),
)


PHASE3_MOTION_PARAMETERS = Phase3MotionParameters(
    working_area_mm=(200.0, 150.0),
    screened_travel_mm=(220.0, 170.0, 40.0),
    moving_bed_support_mm=(240.0, 190.0, 8.0),
    spoilboard_envelope_mm=(240.0, 190.0, 12.0),
    pcb_edge_margin_mm=(20.0, 20.0),
    nominal_moving_bed_mass_kg=1.24,
    tool_point_test_load_n=5.0,
    tool_point_overhang_mm=50.0,
    rail_classes=PHASE3_RAIL_CLASSES,
    axes=(
        Phase3AxisParameters(
            axis="X",
            travel_mm=220.0,
            rail_class="MGN12H",
            rail_count=2,
            carriages_per_rail=2,
            rail_center_spacing_mm=60.0,
            rail_length_mm=300.0,
            screw_lead_mm=4.0,
            screw_length_mm=300.0,
            screw_unsupported_length_mm=300.0,
            screw_design_force_n=50.0,
            commissioning_feed_mm_min=600.0,
            home_direction="negative X / left",
            fixed_bearing_location="left motor end",
            floating_bearing_location="right end",
        ),
        Phase3AxisParameters(
            axis="Y",
            travel_mm=170.0,
            rail_class="MGN12H",
            rail_count=2,
            carriages_per_rail=2,
            rail_center_spacing_mm=220.0,
            rail_length_mm=280.0,
            screw_lead_mm=4.0,
            screw_length_mm=280.0,
            screw_unsupported_length_mm=280.0,
            screw_design_force_n=50.0,
            commissioning_feed_mm_min=700.0,
            home_direction="negative Y / front; moving bed travels with Y",
            fixed_bearing_location="front motor end",
            floating_bearing_location="rear end",
        ),
        Phase3AxisParameters(
            axis="Z",
            travel_mm=40.0,
            rail_class="MGN9H",
            rail_count=2,
            carriages_per_rail=2,
            rail_center_spacing_mm=60.0,
            rail_length_mm=100.0,
            screw_lead_mm=2.0,
            screw_length_mm=120.0,
            screw_unsupported_length_mm=120.0,
            screw_design_force_n=50.0,
            commissioning_feed_mm_min=1200.0,
            home_direction="positive Z / up",
            fixed_bearing_location="upper motor end",
            floating_bearing_location="lower radial support",
        ),
    ),
    screw_candidate_leads_mm=(2.0, 4.0),
    screw_root_diameter_mm=6.2,
    screw_youngs_modulus_n_per_mm2=200000.0,
    screw_density_kg_per_mm3=7.85e-6,
    screw_efficiency=0.35,
    critical_speed_margin=0.70,
    motor_steps_per_revolution=200,
    recommended_microsteps=8,
    motor_mounting_square_mm=42.3,
    motor_body_length_range_mm=(40.0, 48.0),
    motor_shaft_diameter_mm=5.0,
    motor_shaft_engagement_mm=20.0,
    minimum_xy_holding_torque_nm=0.45,
    minimum_z_holding_torque_nm=0.55,
    motor_phase_current_screening_range_a=(0.8, 1.5),
    bearing_bore_mm=8.0,
    fixed_bearing_strategy="paired angular-contact or compact BK08-class fixed support; vendor and fit remain open",
    floating_bearing_strategy="8 mm radial BF08-class support with axial float; do not clamp both screw ends",
    coupler_strategy="flexible 5 mm motor to 8 mm screw coupler; torque transmission only, never an axial bearing",
    nut_strategy_xy="adjustable spring-preloaded split brass or dual-brass anti-backlash nut; replaceable and measurable",
    nut_strategy_z="adjustable preloaded anti-backlash nut only after drag and gravity-hold test; standard brass is a fallback",
    backlash_target_mm=0.030,
    controller_family="GRBL 1.1-compatible STEP/DIR controller; exact Arduino CNC Shield revision is unresolved",
    driver_candidates=("A4988", "DRV8825"),
    driver_microstep_limits=(("A4988", 16), ("DRV8825", 32)),
    controller_required_interfaces=(
        "three independent STEP/DIR axis channels",
        "X/Y/Z homing and hard-limit inputs",
        "conductive probe input with fault-safe wiring",
        "spindle enable and PWM or documented external speed control",
        "12-24 V motor supply and verified driver cooling/current setting",
    ),
    controller_identification_checklist=(
        "record shield revision and pinout",
        "record GRBL fork and firmware version",
        "identify driver carrier and current-limit method",
        "measure available motor supply voltage and current margin",
        "verify limit, probe, spindle-enable, and PWM pins electrically",
        "verify homing direction, pull-off, debounce, soft-limit, and alarm behavior",
    ),
    home_positions=(
        ("X", "negative / left end"),
        ("Y", "negative / front end of moving bed"),
        ("Z", "positive / upper safe end"),
    ),
    machine_coordinate_definition="After homing, MCS is anchored by the three switch datums. With standard GRBL homing, negative-home X/Y report approximately -$27 after pull-off and increase away from the switches; positive-home Z reports approximately $132+$27 at the upper switch and decreases toward the bed. Soft limits are enabled only after switch locations and travel are measured.",
    work_coordinate_definition="G54 work zero is set on the registered PCB datum, normally the front-left board corner in X/Y and the probed copper or board surface in Z. Cutting remains a negative-Z work move from the surface.",
    machine_envelope_mm=(400.0, 400.0, 310.0),
    service_footprint_mm=(520.0, 520.0, 370.0),
    rail_reference_envelopes_mm=(
        ("MGN9H", (9.0, 1.8)),
        ("MGN12H", (12.0, 2.5)),
    ),
    reference_screw_diameter_mm=8.0,
    reference_nut_envelope_mm=(18.0, 18.0, 18.0),
    reference_motor_envelope_mm=(42.3, 42.3, 48.0),
    reference_bearing_support_envelopes_mm=(
        ("X", (20.0, 42.0, 30.0)),
        ("Y", (42.0, 20.0, 30.0)),
        ("Z", (42.0, 42.0, 20.0)),
    ),
    reference_lower_bearing_support_envelope_mm=(30.0, 30.0, 16.0),
    reference_coupler_envelopes_mm=(
        ("X", (24.0, 20.0, 20.0)),
        ("Y", (20.0, 24.0, 20.0)),
        ("Z", (20.0, 20.0, 24.0)),
    ),
    spindle_mount_envelope_mm=(52.0, 52.0, 20.0),
    x_rail_center_y_mm=-48.0,
    x_rail_center_z_mm=130.0,
    y_rail_center_z_mm=-19.0,
    z_rail_center_y_mm=-20.0,
    z_rail_base_z_mm=80.0,
    z_screw_center_offset_y_mm=-16.0,
    y_carriage_center_offsets_mm=(-50.0, 50.0),
    reference_end_clearance_mm=10.0,
    reference_lower_support_overlap_mm=2.0,
    reference_motor_clearance_mm=2.0,
    spindle_mount_min_z_mm=118.0,
    physical_motion_tests=(
        "rail-seat flatness and carriage play after preload",
        "screw backlash and reversal hysteresis in both directions",
        "anti-backlash nut preload, drag, and wear after cycling",
        "fixed-end axial play and floating-end thermal movement",
        "homing repeatability and switch fault response",
        "missed-step margin at commissioning feed and acceleration",
        "axis straightness, squareness, and calibrated absolute error",
        "5 N tool-point deflection in X/Y/Z with the selected spindle envelope",
    ),
    source_urls=(
        "https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf",
        "https://www.allegromicro.com/en/products/motor-drivers/brush-dc-motor-drivers/a4988",
        "https://www.ti.com/lit/ds/symlink/drv8825.pdf",
        "https://github.com/gnea/grbl/blob/master/doc/markdown/settings.md?plain=1",
        "https://github.com/gnea/grbl/blob/master/doc/markdown/interface.md",
    ),
)


@dataclass(frozen=True)
class Phase3APackagingVariant:
    """Review-only packaging inputs for the Phase 3A compacting study.

    The Phase 3 axis classes remain the source of truth for rail family,
    guide count, screw lead, bearing topology, and motor class.  This record
    contains only packaging alternatives around that baseline.  It is not a
    production-part definition.
    """

    variant_id: str
    title: str
    design_intent: str
    working_area_mm: tuple[float, float]
    tool_travel_mm: tuple[float, float, float]
    bed_support_mm: tuple[float, float, float]
    spoilboard_mm: tuple[float, float, float]
    pcb_edge_margin_mm: tuple[float, float]
    rail_lengths_mm: tuple[float, float, float]
    screw_lengths_mm: tuple[float, float, float]
    screw_unsupported_lengths_mm: tuple[float, float, float]
    rail_end_margin_mm: tuple[float, float, float]
    x_carriage_center_offsets_mm: tuple[float, float]
    y_carriage_center_offsets_mm: tuple[float, float]
    z_carriage_center_offsets_mm: tuple[float, float]
    commissioning_feeds_mm_min: tuple[float, float, float]
    body_envelope_mm: tuple[float, float, float]
    body_min_z_mm: float
    body_max_z_mm: float
    service_footprint_mm: tuple[float, float, float]
    x_rail_center_y_mm: float
    x_rail_center_z_mm: float
    y_rail_center_z_mm: float
    z_rail_center_y_mm: float
    z_screw_center_z_mm: float
    z_screw_center_offset_y_mm: float
    y_motor_center_z_mm: float
    bed_sweep_end_clearance_mm: float
    bed_to_y_motor_clearance_mm: float
    x_motor_recess_mm: float
    y_motor_protrusion_mm: float
    gantry_outer_width_mm: float
    gantry_side_width_mm: float
    gantry_depth_mm: float
    gantry_bottom_z_mm: float
    gantry_height_mm: float
    bearing_fixed_envelopes_mm: tuple[tuple[str, tuple[float, float, float]], ...]
    bearing_floating_envelopes_mm: tuple[tuple[str, tuple[float, float, float]], ...]
    bearing_strategy: str
    motor_strategies: tuple[tuple[str, str], ...]
    home_limit_clearance_mm: float
    largest_future_petg_print_mm: tuple[float, float, float]
    largest_future_petg_print_notes: str
    evidence_status: ParameterStatus = ParameterStatus.PRELIMINARY


PHASE3A_PACKAGING_VARIANTS = (
    Phase3APackagingVariant(
        variant_id="P1",
        title="conservative serviceable",
        design_intent=(
            "Retain generous PCB and carriage margins, conventional external access, "
            "and the least aggressive motor recessing."
        ),
        working_area_mm=(200.0, 150.0),
        tool_travel_mm=(220.0, 170.0, 40.0),
        bed_support_mm=(240.0, 190.0, 8.0),
        spoilboard_mm=(240.0, 190.0, 12.0),
        pcb_edge_margin_mm=(20.0, 20.0),
        rail_lengths_mm=(370.0, 340.0, 145.0),
        screw_lengths_mm=(390.0, 360.0, 160.0),
        screw_unsupported_lengths_mm=(370.0, 340.0, 145.0),
        rail_end_margin_mm=(10.0, 10.0, 5.0),
        x_carriage_center_offsets_mm=(-40.0, 40.0),
        y_carriage_center_offsets_mm=(-50.0, 50.0),
        z_carriage_center_offsets_mm=(-25.0, 25.0),
        commissioning_feeds_mm_min=(450.0, 550.0, 1200.0),
        body_envelope_mm=(394.0, 385.0, 296.0),
        body_min_z_mm=-56.0,
        body_max_z_mm=240.0,
        service_footprint_mm=(474.0, 465.0, 344.0),
        x_rail_center_y_mm=-36.0,
        x_rail_center_z_mm=96.0,
        y_rail_center_z_mm=-14.0,
        z_rail_center_y_mm=-20.0,
        z_screw_center_z_mm=96.0,
        z_screw_center_offset_y_mm=-12.0,
        y_motor_center_z_mm=-34.0,
        bed_sweep_end_clearance_mm=12.5,
        bed_to_y_motor_clearance_mm=4.0,
        x_motor_recess_mm=12.0,
        y_motor_protrusion_mm=22.0,
        gantry_outer_width_mm=370.0,
        gantry_side_width_mm=18.0,
        gantry_depth_mm=76.0,
        gantry_bottom_z_mm=58.0,
        gantry_height_mm=58.0,
        bearing_fixed_envelopes_mm=(
            ("X", (22.0, 42.0, 30.0)),
            ("Y", (42.0, 22.0, 30.0)),
            ("Z", (42.0, 42.0, 26.0)),
        ),
        bearing_floating_envelopes_mm=(
            ("X", (18.0, 30.0, 18.0)),
            ("Y", (30.0, 18.0, 18.0)),
            ("Z", (30.0, 30.0, 16.0)),
        ),
        bearing_strategy=(
            "BK08/BF08-class service envelopes retained as a conservative screen; "
            "fixed end reacts axial load and floating end is radial-only."
        ),
        motor_strategies=(
            ("X", "direct axial motor in a shallow side pocket with removable outer cover"),
            ("Y", "direct axial motor at the front, partly recessed into the front cross-member"),
            ("Z", "direct axial motor above the upper fixed support with top access"),
        ),
        home_limit_clearance_mm=10.0,
        largest_future_petg_print_mm=(340.0, 80.0, 170.0),
        largest_future_petg_print_notes=(
            "One-piece fixed-gantry torsion-box bound is printable in a 350 mm class "
            "machine only with measured diagonal and brim clearance; split side interfaces remain the fallback."
        ),
    ),
    Phase3APackagingVariant(
        variant_id="P2",
        title="balanced compact/serviceable",
        design_intent=(
            "Reduce footprint through controlled carriage pitch, recessed direct-drive motors, "
            "shorter bearing envelopes, and a 15 mm PCB perimeter while retaining full Phase 3 travel."
        ),
        working_area_mm=(200.0, 150.0),
        tool_travel_mm=(220.0, 170.0, 40.0),
        bed_support_mm=(230.0, 180.0, 8.0),
        spoilboard_mm=(230.0, 180.0, 12.0),
        pcb_edge_margin_mm=(15.0, 15.0),
        rail_lengths_mm=(340.0, 310.0, 130.0),
        screw_lengths_mm=(360.0, 330.0, 145.0),
        screw_unsupported_lengths_mm=(340.0, 310.0, 130.0),
        rail_end_margin_mm=(6.0, 6.0, 5.0),
        x_carriage_center_offsets_mm=(-30.0, 30.0),
        y_carriage_center_offsets_mm=(-40.0, 40.0),
        z_carriage_center_offsets_mm=(-20.0, 20.0),
        commissioning_feeds_mm_min=(520.0, 650.0, 1100.0),
        body_envelope_mm=(364.0, 356.0, 276.0),
        body_min_z_mm=-56.0,
        body_max_z_mm=220.0,
        service_footprint_mm=(444.0, 428.0, 322.0),
        x_rail_center_y_mm=-32.0,
        x_rail_center_z_mm=84.0,
        y_rail_center_z_mm=-14.0,
        z_rail_center_y_mm=-20.0,
        z_screw_center_z_mm=84.0,
        z_screw_center_offset_y_mm=-10.0,
        y_motor_center_z_mm=-34.0,
        bed_sweep_end_clearance_mm=3.0,
        bed_to_y_motor_clearance_mm=4.0,
        x_motor_recess_mm=12.0,
        y_motor_protrusion_mm=19.0,
        gantry_outer_width_mm=344.0,
        gantry_side_width_mm=16.0,
        gantry_depth_mm=68.0,
        gantry_bottom_z_mm=52.0,
        gantry_height_mm=58.0,
        bearing_fixed_envelopes_mm=(
            ("X", (18.0, 30.0, 24.0)),
            ("Y", (30.0, 18.0, 24.0)),
            ("Z", (34.0, 34.0, 24.0)),
        ),
        bearing_floating_envelopes_mm=(
            ("X", (16.0, 24.0, 14.0)),
            ("Y", (24.0, 16.0, 14.0)),
            ("Z", (26.0, 26.0, 14.0)),
        ),
        bearing_strategy=(
            "Use replaceable standardized 8 mm bearing cartridges in printed pockets: "
            "paired axial bearings or a compact angular-contact pair at the fixed end, "
            "single radial bearing with axial float at the far end; housing is not yet production geometry."
        ),
        motor_strategies=(
            ("X", "direct axial motor recessed into the left gantry side with an accessible cover"),
            ("Y", "direct axial motor recessed into the front cross-member; no belt drive"),
            ("Z", "direct axial motor inside an upper pocket with a removable top service plate"),
        ),
        home_limit_clearance_mm=8.0,
        largest_future_petg_print_mm=(330.0, 72.0, 155.0),
        largest_future_petg_print_notes=(
            "A fixed-gantry torsion-box bound can fit the 350 mm Voron class in its long axis; "
            "print orientation, diagonal clearance, inserts, and rail-seat coupons remain to be proven."
        ),
    ),
    Phase3APackagingVariant(
        variant_id="P3",
        title="aggressive minimum practical",
        design_intent=(
            "Approach the minimum practical package with reduced PCB margin, shorter carriage pitch, "
            "tight rail-end margins, and integrated service pockets; use only if P2 evidence is favorable."
        ),
        working_area_mm=(200.0, 150.0),
        tool_travel_mm=(210.0, 160.0, 40.0),
        bed_support_mm=(220.0, 170.0, 8.0),
        spoilboard_mm=(220.0, 170.0, 10.0),
        pcb_edge_margin_mm=(10.0, 10.0),
        rail_lengths_mm=(320.0, 280.0, 125.0),
        screw_lengths_mm=(340.0, 300.0, 140.0),
        screw_unsupported_lengths_mm=(320.0, 280.0, 125.0),
        rail_end_margin_mm=(5.0, 4.0, 2.0),
        x_carriage_center_offsets_mm=(-24.0, 24.0),
        y_carriage_center_offsets_mm=(-30.0, 30.0),
        z_carriage_center_offsets_mm=(-20.0, 20.0),
        commissioning_feeds_mm_min=(580.0, 700.0, 1100.0),
        body_envelope_mm=(344.0, 334.0, 268.0),
        body_min_z_mm=-54.0,
        body_max_z_mm=214.0,
        service_footprint_mm=(414.0, 404.0, 318.0),
        x_rail_center_y_mm=-30.0,
        x_rail_center_z_mm=80.0,
        y_rail_center_z_mm=-13.0,
        z_rail_center_y_mm=-20.0,
        z_screw_center_z_mm=80.0,
        z_screw_center_offset_y_mm=-8.0,
        y_motor_center_z_mm=-32.0,
        bed_sweep_end_clearance_mm=2.0,
        bed_to_y_motor_clearance_mm=2.5,
        x_motor_recess_mm=12.0,
        y_motor_protrusion_mm=16.0,
        gantry_outer_width_mm=324.0,
        gantry_side_width_mm=14.0,
        gantry_depth_mm=64.0,
        gantry_bottom_z_mm=48.0,
        gantry_height_mm=54.0,
        bearing_fixed_envelopes_mm=(
            ("X", (18.0, 26.0, 22.0)),
            ("Y", (26.0, 18.0, 22.0)),
            ("Z", (30.0, 30.0, 22.0)),
        ),
        bearing_floating_envelopes_mm=(
            ("X", (14.0, 22.0, 12.0)),
            ("Y", (22.0, 14.0, 12.0)),
            ("Z", (24.0, 24.0, 12.0)),
        ),
        bearing_strategy=(
            "Printed end pockets use replaceable 8 mm radial/axial bearing cartridges with minimal "
            "external envelope; PETG creep, preload retention, and tool access make this conditional."
        ),
        motor_strategies=(
            ("X", "direct axial motor deeply recessed into the side structure; cover removal is mandatory"),
            ("Y", "direct axial motor inside the front structure; front panel and screw access are constrained"),
            ("Z", "direct axial motor in the smallest upper pocket with top-only service access"),
        ),
        home_limit_clearance_mm=5.0,
        largest_future_petg_print_mm=(320.0, 68.0, 145.0),
        largest_future_petg_print_notes=(
            "Fits the nominal Voron volume on paper, but the tight rail-seat and fastener access make "
            "a split or near-one-piece print more likely until an assembly mock-up passes."
        ),
    ),
)


@dataclass(frozen=True)
class InsertFamilyParameters:
    """Parameterized heat-set insert family boundary for PETG interfaces.

    Supplier-specific dimensions intentionally remain optional.  A screening
    model may use the preliminary wall, edge, and installation-access values,
    but it must not manufacture a pilot pocket until the actual insert is
    selected, measured, and validated on a representative coupon.
    """

    nominal_size: str
    intended_use: str
    outer_diameter_mm: NumericRange | None
    length_mm: NumericRange | None
    pilot_hole_diameter_mm: NumericRange | None
    insertion_depth_mm: NumericRange | None
    minimum_surrounding_wall_mm: float
    minimum_edge_distance_mm: float
    insertion_direction: str
    screw_clearance_diameter_mm: NumericRange | None
    installation_tool_access_mm: tuple[float, float, float]
    evidence_status: ParameterStatus
    notes: str

    @property
    def exact_dimensions_resolved(self) -> bool:
        """Whether all supplier-dependent insert dimensions are available."""

        return all(
            value is not None
            for value in (
                self.outer_diameter_mm,
                self.length_mm,
                self.pilot_hole_diameter_mm,
                self.insertion_depth_mm,
                self.screw_clearance_diameter_mm,
            )
        )


@dataclass(frozen=True)
class FastenerInterfaceParameter:
    """Review-level description of one reusable printed interface."""

    interface_id: str
    function: str
    fastening_mode: str
    insert_size: str | None
    boss_wall_mm: float
    edge_distance_mm: float
    installation_tool_access_mm: tuple[float, float, float]
    load_transfer_features: tuple[str, ...]
    serviceable: bool
    requires_selected_insert: bool = True
    size_justification: str | None = None
    through_bolt_justification: str | None = None
    notes: str = ""


@dataclass(frozen=True)
class FastenerStrategyParameters:
    """Central PETG fastening strategy used by Phase 3A and later phases."""

    allowed_insert_sizes: tuple[str, ...]
    default_size_by_use: tuple[tuple[str, str], ...]
    insert_families: tuple[InsertFamilyParameters, ...]
    geometric_load_transfer_features: tuple[str, ...]
    through_bolt_reserved_for: tuple[str, ...]
    serviceable_components: tuple[str, ...]
    core_principle: str
    evidence_status: ParameterStatus


PETG_FASTENER_CORE_PRINCIPLE = (
    "Fasteners provide preload; printed geometry provides location and shear "
    "transfer. Heat-set inserts are the default reusable threaded interface "
    "in PETG. Through-bolts are reserved for structural joints where insert "
    "pull-out, creep, preload, or joint moment capacity makes them necessary."
)


PHASE3A_FASTENER_STRATEGY = FastenerStrategyParameters(
    allowed_insert_sizes=("M3", "M4", "M5"),
    default_size_by_use=(
        ("small covers, sensors, limits, probe hardware, and accessories", "M3"),
        ("general structural, motor, bearing, spindle, and module joints", "M4"),
        ("high-load structural joints only when technically justified", "M5"),
    ),
    insert_families=(
        InsertFamilyParameters(
            nominal_size="M3",
            intended_use="Small covers, sensors, limits, probe hardware, and accessories.",
            outer_diameter_mm=None,
            length_mm=None,
            pilot_hole_diameter_mm=None,
            insertion_depth_mm=None,
            minimum_surrounding_wall_mm=3.0,
            minimum_edge_distance_mm=4.0,
            insertion_direction="normal to the boss face where possible; avoid direct pull-out",
            screw_clearance_diameter_mm=None,
            installation_tool_access_mm=(12.0, 12.0, 12.0),
            evidence_status=ParameterStatus.ASSUMPTION,
            notes="Preliminary geometry screen only; replace with measured insert and coupon data.",
        ),
        InsertFamilyParameters(
            nominal_size="M4",
            intended_use="General structural, motor, bearing, spindle, and module joints.",
            outer_diameter_mm=None,
            length_mm=None,
            pilot_hole_diameter_mm=None,
            insertion_depth_mm=None,
            minimum_surrounding_wall_mm=4.0,
            minimum_edge_distance_mm=6.0,
            insertion_direction="normal to the boss face where possible; avoid direct pull-out",
            screw_clearance_diameter_mm=None,
            installation_tool_access_mm=(14.0, 14.0, 14.0),
            evidence_status=ParameterStatus.ASSUMPTION,
            notes="Preliminary geometry screen only; replace with measured insert and coupon data.",
        ),
        InsertFamilyParameters(
            nominal_size="M5",
            intended_use="High-load structural joints only after an explicit load-path review.",
            outer_diameter_mm=None,
            length_mm=None,
            pilot_hole_diameter_mm=None,
            insertion_depth_mm=None,
            minimum_surrounding_wall_mm=5.0,
            minimum_edge_distance_mm=8.0,
            insertion_direction="normal to the boss face where possible; avoid direct pull-out",
            screw_clearance_diameter_mm=None,
            installation_tool_access_mm=(16.0, 16.0, 16.0),
            evidence_status=ParameterStatus.ASSUMPTION,
            notes="Preliminary geometry screen only; M5 is not a default structural fastener.",
        ),
    ),
    geometric_load_transfer_features=(
        "shoulder",
        "step",
        "tongue-and-groove",
        "key",
        "boss",
        "pocket",
        "registration",
        "shear key",
        "mating planar surface",
        "interlocking rib",
    ),
    through_bolt_reserved_for=(
        "insert pull-out or PETG creep is unacceptable",
        "high bending moment or clamping force exceeds the insert interface",
        "cyclic loading or failure consequence requires a more robust load path",
    ),
    serviceable_components=(
        "motors",
        "rails",
        "carriages",
        "lead screws and nuts",
        "bearings",
        "spindle",
        "limit switches",
        "probe and moving-bed wiring",
    ),
    core_principle=PETG_FASTENER_CORE_PRINCIPLE,
    evidence_status=ParameterStatus.PRELIMINARY,
)


PHASE3A_FASTENER_INTERFACE_SCREENS = (
    FastenerInterfaceParameter(
        interface_id="gantry_crossmember_joint",
        function="Seat the fixed gantry crossmember and clamp it for preload.",
        fastening_mode="insert",
        insert_size="M4",
        boss_wall_mm=5.0,
        edge_distance_mm=8.0,
        installation_tool_access_mm=(18.0, 18.0, 18.0),
        load_transfer_features=("deep tongue-and-groove", "stepped shoulder", "interlocking rib"),
        serviceable=True,
        notes="The crossmember must be mechanically seated; it must not hang from M5 screws.",
    ),
    FastenerInterfaceParameter(
        interface_id="x_motor_mount",
        function="Removable X motor pocket and coaxial motor face.",
        fastening_mode="insert",
        insert_size="M4",
        boss_wall_mm=4.5,
        edge_distance_mm=6.0,
        installation_tool_access_mm=(16.0, 16.0, 16.0),
        load_transfer_features=("motor-face shoulder", "planar seat", "pocket side keys"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="y_motor_mount",
        function="Removable front Y motor pocket and coaxial motor face.",
        fastening_mode="insert",
        insert_size="M4",
        boss_wall_mm=4.5,
        edge_distance_mm=6.0,
        installation_tool_access_mm=(16.0, 16.0, 16.0),
        load_transfer_features=("motor-face shoulder", "planar seat", "pocket side keys"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="z_motor_mount",
        function="Removable upper Z motor service plate and coaxial motor face.",
        fastening_mode="insert",
        insert_size="M4",
        boss_wall_mm=4.5,
        edge_distance_mm=6.0,
        installation_tool_access_mm=(16.0, 16.0, 16.0),
        load_transfer_features=("motor-face shoulder", "planar seat", "removable cover step"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="bearing_support_mount",
        function="Replaceable fixed/floating bearing cartridge support.",
        fastening_mode="insert",
        insert_size="M4",
        boss_wall_mm=5.0,
        edge_distance_mm=7.0,
        installation_tool_access_mm=(18.0, 18.0, 18.0),
        load_transfer_features=("bearing pocket", "radial shoulder", "axial seating face"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="rail_mount",
        function="Serviceable rail clamp on a continuous supported rail seat.",
        fastening_mode="insert",
        insert_size="M3",
        boss_wall_mm=3.5,
        edge_distance_mm=5.0,
        installation_tool_access_mm=(14.0, 14.0, 14.0),
        load_transfer_features=("continuous rail shoulder", "planar rail seat", "registration keys"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="spindle_mount",
        function="Replaceable spindle mount with a distributed force loop.",
        fastening_mode="insert",
        insert_size="M4",
        boss_wall_mm=5.0,
        edge_distance_mm=7.0,
        installation_tool_access_mm=(18.0, 18.0, 18.0),
        load_transfer_features=("spindle saddle", "clamp shoulder", "anti-rotation key"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="limit_probe_accessory_mount",
        function="Replaceable limit, probe, cable, and small accessory mounts.",
        fastening_mode="insert",
        insert_size="M3",
        boss_wall_mm=3.0,
        edge_distance_mm=4.0,
        installation_tool_access_mm=(12.0, 12.0, 12.0),
        load_transfer_features=("registration shoulder", "keyed pocket"),
        serviceable=True,
    ),
    FastenerInterfaceParameter(
        interface_id="conditional_high_load_structural_joint",
        function="Conditional escalation example for a joint whose measured load path exceeds M4 insert capacity.",
        fastening_mode="insert",
        insert_size="M5",
        boss_wall_mm=6.0,
        edge_distance_mm=9.0,
        installation_tool_access_mm=(20.0, 20.0, 20.0),
        load_transfer_features=("deep shoulder", "shear key", "large mating planar surface"),
        serviceable=True,
        size_justification="Use M5 only after load, creep, preload, and joint-moment evidence shows M4 is inadequate.",
        notes="Screening example only; this is not a selected production joint.",
    ),
)
