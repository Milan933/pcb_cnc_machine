"""Preliminary Phase 4 structural assembly and gantry-joint study.

This module combines the actual Phase 4 printed structural concept with the
accepted P2 motion and hardware reference envelopes.  It deliberately keeps
component boundaries intact: overlap between a printed interface and a
reference envelope is useful packaging evidence, while overlap between two
independent printed parts must be explicitly justified.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cad.architecture import ArchitectureId
from cad.packaging_phase3a import phase3a_variant_by_id
from cad.parameters import PHASE3A_PACKAGING_VARIANTS

from .architecture_skeleton import (
    SkeletonComponent,
    _build123d,
    _box,
    find_interferences,
    unexpected_interferences,
)
from .packaging_skeleton import build_packaging_skeleton
from cad.parts.phase4_structural import (
    _closed_box,
    _compound,
    build_phase4_structural_parts,
)


@dataclass(frozen=True)
class Phase4AssemblyModel:
    """Preliminary structural assembly with explicit interference semantics."""

    candidate_id: ArchitectureId
    components: tuple[SkeletonComponent, ...]
    expected_interference_pairs: tuple[frozenset[str], ...]
    variant: str = "phase4-p2-preliminary"
    structural_parts: tuple[SkeletonComponent, ...] = ()

    @property
    def compound(self) -> Any:
        build123d = _build123d()
        return build123d.Compound(children=[component.shape for component in self.components])

    @property
    def bounding_box_mm(self) -> dict[str, tuple[float, float, float]]:
        bounding_box = self.compound.bounding_box()

        def vector_tuple(vector: Any) -> tuple[float, float, float]:
            return tuple(float(getattr(vector, axis)) for axis in ("X", "Y", "Z"))

        return {
            "min": vector_tuple(bounding_box.min),
            "max": vector_tuple(bounding_box.max),
            "size": vector_tuple(bounding_box.size),
        }


def _pairs(*pairs: tuple[str, str]) -> tuple[frozenset[str], ...]:
    return tuple(frozenset(pair) for pair in pairs)


def phase4_expected_interference_pairs() -> tuple[frozenset[str], ...]:
    """Return only intentional solid overlaps between separate concept parts.

    The list is intentionally narrow.  Motion references are excluded by the
    shared interference helper, but two independent printed solids are only
    allowed to overlap where the concept explicitly models a load-transfer or
    service interface.
    """

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
        ("x_fixed_bearing_cartridge", "gantry_beam_left"),
        ("x_floating_bearing_cartridge", "gantry_beam_right"),
        ("x_carriage_plate", "gantry_beam_left"),
        ("x_carriage_plate", "gantry_beam_right"),
        ("z_carriage_plate", "gantry_beam_left"),
        ("z_carriage_plate", "gantry_beam_right"),
        ("x_carriage_plate", "z_carriage_plate"),
        ("x_carriage_plate", "z_fixed_bearing_support"),
        ("z_carriage_plate", "z_fixed_bearing_support"),
        ("z_carriage_plate", "spindle_mount_concept"),
        ("x_carriage_plate", "spindle_mount_concept"),
    )


def build_phase4_assembly() -> Phase4AssemblyModel:
    """Build Phase 4 structural parts plus the accepted P2 references."""

    selected = phase3a_variant_by_id("P2", PHASE3A_PACKAGING_VARIANTS)
    packaging = build_packaging_skeleton(selected)
    # Replace the old outer structural bound with the actual Phase 4 concept;
    # retain motion, process, and hardware envelopes for clearance review.
    references = tuple(component for component in packaging.components if component.category != "structural")
    structural_parts = build_phase4_structural_parts()
    return Phase4AssemblyModel(
        candidate_id=ArchitectureId.A,
        components=structural_parts + references,
        expected_interference_pairs=phase4_expected_interference_pairs(),
        structural_parts=structural_parts,
    )


def build_gantry_joint_study() -> Phase4AssemblyModel:
    """Build separated J1/J2/J3 comparison solids for review export."""

    build123d = _build123d()
    components: list[SkeletonComponent] = []
    origins = {"J1": -230.0, "J2": -70.0, "J3": 90.0}
    notes = {
        "J1": "Deep tongue/socket: geometry carries shear and torsion; clamp inserts supply preload.",
        "J2": "Stepped keyed shoulder: broad shoulder carries bending and a positive key carries shear.",
        "J3": "Distributed rib/shear-key interface: several ribs share the joint reaction.",
    }
    for concept_id, origin_x in origins.items():
        left = _closed_box(build123d, f"{concept_id}_left", (70.0, 70.0, 60.0), (origin_x, -35.0, 0.0), 5.0)
        right = _closed_box(build123d, f"{concept_id}_right", (70.0, 70.0, 60.0), (origin_x + 70.0, -35.0, 0.0), 5.0)
        if concept_id == "J1":
            tongue = _box(build123d, "J1_tongue", (12.0, 40.0, 42.0), (origin_x + 58.0, -20.0, 9.0))
            socket = _box(build123d, "J1_socket", (12.0, 40.0, 42.0), (origin_x + 70.0, -20.0, 9.0))
            right = right.cut(socket)
            pieces = [left, tongue, right]
        elif concept_id == "J2":
            shoulder = _box(build123d, "J2_shoulder", (16.0, 56.0, 30.0), (origin_x + 58.0, -28.0, 15.0))
            key = _box(build123d, "J2_key", (8.0, 24.0, 24.0), (origin_x + 66.0, -12.0, 18.0))
            pieces = [left, shoulder, right, key]
        else:
            ribs = [
                _box(build123d, f"J3_rib_{index}", (10.0, 14.0, 42.0), (origin_x + 58.0, y, 9.0))
                for index, y in enumerate((-27.0, -7.0, 13.0), start=1)
            ]
            pieces = [left, right, *ribs]
        shape = _compound(build123d, f"joint_{concept_id}", pieces)
        components.append(
            SkeletonComponent(
                name=f"joint_{concept_id}",
                category="joint-study",
                shape=shape,
                notes=notes[concept_id],
            )
        )
    return Phase4AssemblyModel(
        candidate_id=ArchitectureId.A,
        components=tuple(components),
        expected_interference_pairs=tuple(),
        variant="phase4-gantry-joint-study",
    )


def export_phase4_review_geometry(model: Phase4AssemblyModel, output_dir: Path) -> dict[str, Path]:
    """Export review-only STEP/STL assembly and individual structural parts."""

    build123d = _build123d()
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
    # build123d 0.12.0 may consume the child topology while writing a large
    # Compound STEP.  Export the individually named solids first so the
    # assembly derivative cannot invalidate their review exports.
    assembly_step = output_dir / f"{model.variant}.step"
    assembly_stl = output_dir / f"{model.variant}.stl"
    build123d.export_step(model.compound, assembly_step)
    build123d.export_stl(model.compound, assembly_stl, tolerance=0.01, angular_tolerance=0.2)
    exports["assembly_step"] = assembly_step
    exports["assembly_stl"] = assembly_stl
    return exports


def export_gantry_joint_study(model: Phase4AssemblyModel, output_dir: Path) -> dict[str, Path]:
    """Export the separated joint comparison geometry."""

    build123d = _build123d()
    output_dir.mkdir(parents=True, exist_ok=True)
    exports: dict[str, Path] = {}
    step_path = output_dir / f"{model.variant}.step"
    stl_path = output_dir / f"{model.variant}.stl"
    build123d.export_step(model.compound, step_path)
    build123d.export_stl(model.compound, stl_path, tolerance=0.01, angular_tolerance=0.2)
    exports["joint_study_step"] = step_path
    exports["joint_study_stl"] = stl_path
    return exports


def phase4_model_interferences(model: Phase4AssemblyModel) -> tuple[dict[str, Any], ...]:
    """Expose the shared solid-overlap screen for the Phase 4 model."""

    # ``find_interferences`` consumes the same small structural-model
    # contract; the Phase4 dataclass intentionally provides that contract.
    return unexpected_interferences(model)  # type: ignore[arg-type]


__all__ = [
    "Phase4AssemblyModel",
    "build_gantry_joint_study",
    "build_phase4_assembly",
    "export_gantry_joint_study",
    "export_phase4_review_geometry",
    "find_interferences",
    "phase4_expected_interference_pairs",
    "phase4_model_interferences",
]
