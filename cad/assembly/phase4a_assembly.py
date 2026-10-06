"""Phase 4A optimized structural assembly and review exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cad.architecture import ArchitectureId
from cad.parameters import PHASE3A_PACKAGING_VARIANTS

from .architecture_skeleton import (
    SkeletonComponent,
    find_interferences,
    unexpected_interferences,
)
from .packaging_skeleton import build_packaging_skeleton
from .phase4_assembly import Phase4AssemblyModel, build_gantry_joint_study
from cad.packaging_phase3a import phase3a_variant_by_id
from cad.parts.phase4a_structural import (
    SELECTED_PHASE4A_VARIANT,
    build_phase4a_structural_parts,
)


def _pairs(*pairs: tuple[str, str]) -> tuple[frozenset[str], ...]:
    return tuple(frozenset(pair) for pair in pairs)


def phase4a_expected_interference_pairs(variant_id: str = SELECTED_PHASE4A_VARIANT) -> tuple[frozenset[str], ...]:
    """Return documented overlap interfaces for one optimized assembly."""

    if variant_id == "O1":
        return _pairs(
            ("base_y_rail_carrier_left", "base_front_left"),
            ("base_y_rail_carrier_left", "base_rear_left"),
            ("base_y_rail_carrier_right", "base_front_right"),
            ("base_y_rail_carrier_right", "base_rear_right"),
            ("base_center_tie", "base_y_rail_carrier_left"),
            ("base_center_tie", "base_y_rail_carrier_right"),
            ("y_motor_service_pocket", "base_front_left"),
            ("y_motor_service_pocket", "base_front_right"),
            ("y_fixed_bearing_cartridge", "base_front_left"),
            ("y_fixed_bearing_cartridge", "base_front_right"),
            ("y_floating_bearing_cartridge", "base_rear_left"),
            ("y_floating_bearing_cartridge", "base_rear_right"),
            ("machine_foot_front_left", "base_front_left"),
            ("machine_foot_front_right", "base_front_right"),
            ("machine_foot_rear_left", "base_rear_left"),
            ("machine_foot_rear_right", "base_rear_right"),
            ("base_left_side_member", "machine_foot_front_left"),
            ("base_left_side_member", "machine_foot_rear_left"),
            ("base_right_side_member", "machine_foot_front_right"),
            ("base_right_side_member", "machine_foot_rear_right"),
            ("base_y_rail_carrier_left", "gantry_tower_left"),
            ("base_y_rail_carrier_right", "gantry_tower_right"),
            ("y_motor_service_pocket", "y_fixed_bearing_cartridge"),
            ("gantry_beam_left", "x_fixed_bearing_cartridge"),
            ("gantry_beam_right", "x_floating_bearing_cartridge"),
            ("gantry_beam_left", "x_z_backbone"),
            ("gantry_beam_right", "x_z_backbone"),
            ("gantry_beam_left", "z_carriage_plate"),
            ("gantry_beam_right", "z_carriage_plate"),
            ("x_z_backbone", "z_carriage_plate"),
            ("x_z_backbone", "spindle_mount_concept"),
            ("z_carriage_plate", "spindle_mount_concept"),
        )
    if variant_id == "O2":
        return _pairs(
            ("base_left_integrated", "base_center_tie"),
            ("base_right_integrated", "base_center_tie"),
            ("base_left_integrated", "y_motor_service_pocket"),
            ("base_right_integrated", "y_motor_service_pocket"),
            ("base_left_integrated", "y_fixed_bearing_cartridge"),
            ("base_right_integrated", "y_fixed_bearing_cartridge"),
            ("base_left_integrated", "y_floating_bearing_cartridge"),
            ("base_right_integrated", "y_floating_bearing_cartridge"),
            ("base_left_integrated", "machine_foot_front_left"),
            ("base_left_integrated", "machine_foot_rear_left"),
            ("base_right_integrated", "machine_foot_front_right"),
            ("base_right_integrated", "machine_foot_rear_right"),
            ("base_left_integrated", "gantry_left_integrated"),
            ("base_right_integrated", "gantry_right_integrated"),
            ("gantry_left_integrated", "x_fixed_bearing_cartridge"),
            ("gantry_right_integrated", "x_floating_bearing_cartridge"),
            ("gantry_left_integrated", "x_z_backbone"),
            ("gantry_right_integrated", "x_z_backbone"),
            ("gantry_left_integrated", "z_carriage_plate"),
            ("gantry_right_integrated", "z_carriage_plate"),
            ("x_z_backbone", "z_carriage_plate"),
            ("x_z_backbone", "spindle_mount_concept"),
            ("z_carriage_plate", "spindle_mount_concept"),
            ("y_motor_service_pocket", "y_fixed_bearing_cartridge"),
        )
    if variant_id == "O3":
        return _pairs(
            ("base_gantry_left", "base_center_tie"),
            ("base_gantry_right", "base_center_tie"),
            ("base_gantry_left", "y_motor_service_pocket"),
            ("base_gantry_right", "y_motor_service_pocket"),
            ("base_gantry_left", "y_fixed_bearing_cartridge"),
            ("base_gantry_right", "y_fixed_bearing_cartridge"),
            ("base_gantry_left", "y_floating_bearing_cartridge"),
            ("base_gantry_right", "y_floating_bearing_cartridge"),
            ("base_gantry_left", "x_z_backbone"),
            ("base_gantry_right", "x_z_backbone"),
            ("base_gantry_left", "z_carriage_plate"),
            ("base_gantry_right", "z_carriage_plate"),
            ("x_z_backbone", "z_carriage_plate"),
            ("x_z_backbone", "spindle_mount_concept"),
            ("z_carriage_plate", "spindle_mount_concept"),
            ("y_motor_service_pocket", "y_fixed_bearing_cartridge"),
        )
    raise ValueError(f"Unknown Phase 4A variant: {variant_id}")


def build_phase4a_assembly(
    variant_id: str = SELECTED_PHASE4A_VARIANT,
    structural_parts: tuple[SkeletonComponent, ...] | None = None,
) -> Phase4AssemblyModel:
    """Build the optimized structural parts with the unchanged P2 references."""

    selected = phase3a_variant_by_id("P2", PHASE3A_PACKAGING_VARIANTS)
    packaging = build_packaging_skeleton(selected)
    references = tuple(component for component in packaging.components if component.category != "structural")
    structural_parts = structural_parts or build_phase4a_structural_parts(variant_id)
    return Phase4AssemblyModel(
        candidate_id=ArchitectureId.A,
        components=structural_parts + references,
        expected_interference_pairs=phase4a_expected_interference_pairs(variant_id),
        variant=f"phase4a-{variant_id.lower()}-p2",
        structural_parts=structural_parts,
    )


def phase4a_model_interferences(model: Phase4AssemblyModel) -> tuple[dict[str, Any], ...]:
    """Return only unexpected structural overlaps for a Phase 4A model."""

    return unexpected_interferences(model)  # type: ignore[arg-type]


def export_phase4a_review_geometry(model: Phase4AssemblyModel, output_dir: Path) -> dict[str, Path]:
    """Export selected Phase 4A review geometry to an explicit temporary directory."""

    import build123d

    output_dir.mkdir(parents=True, exist_ok=True)
    exports: dict[str, Path] = {}
    for component in model.structural_parts:
        stem = f"{model.variant}-{component.name}"
        step_path = output_dir / f"{stem}.step"
        stl_path = output_dir / f"{stem}.stl"
        build123d.export_step(component.shape, step_path)
        build123d.export_stl(component.shape, stl_path, tolerance=0.01, angular_tolerance=0.2)
        exports[f"{component.name}_step"] = step_path
        exports[f"{component.name}_stl"] = stl_path
    assembly_step = output_dir / f"{model.variant}.step"
    assembly_stl = output_dir / f"{model.variant}.stl"
    build123d.export_step(model.compound, assembly_step)
    build123d.export_stl(model.compound, assembly_stl, tolerance=0.01, angular_tolerance=0.2)
    exports["assembly_step"] = assembly_step
    exports["assembly_stl"] = assembly_stl
    return exports


__all__ = [
    "build_gantry_joint_study",
    "build_phase4a_assembly",
    "export_phase4a_review_geometry",
    "find_interferences",
    "phase4a_expected_interference_pairs",
    "phase4a_model_interferences",
]
