"""Generate tracked Phase 4 owner-review views and machine-readable metrics.

The source geometry is the current preliminary build123d assembly.  The
images are deliberately simple engineering projections generated from the
actual OCCT tessellation; they are review illustrations, not release
drawings, photorealistic renders, or manufacturing evidence.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw

from cad.assembly.phase4_assembly import build_phase4_assembly
from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS as P
from cad.phase4_calculations import phase4_structural_estimate


Vec3 = tuple[float, float, float]
Vec2 = tuple[float, float]


CLASSIFICATION = {
    "base_front_left": "CRITICAL STRUCTURAL",
    "base_front_right": "CRITICAL STRUCTURAL",
    "base_rear_left": "CRITICAL STRUCTURAL",
    "base_rear_right": "CRITICAL STRUCTURAL",
    "base_left_side_member": "CRITICAL STRUCTURAL",
    "base_right_side_member": "CRITICAL STRUCTURAL",
    "base_y_rail_carrier_left": "CRITICAL STRUCTURAL",
    "base_y_rail_carrier_right": "CRITICAL STRUCTURAL",
    "base_center_tie": "CRITICAL STRUCTURAL",
    "gantry_tower_left": "CRITICAL STRUCTURAL",
    "gantry_tower_right": "CRITICAL STRUCTURAL",
    "gantry_beam_left": "CRITICAL STRUCTURAL",
    "gantry_beam_right": "CRITICAL STRUCTURAL",
    "x_carriage_plate": "CRITICAL STRUCTURAL",
    "z_carriage_plate": "CRITICAL STRUCTURAL",
    "moving_bed_frame": "CRITICAL STRUCTURAL",
    "y_motor_service_pocket": "SECONDARY STRUCTURAL",
    "y_fixed_bearing_cartridge": "SECONDARY STRUCTURAL",
    "y_floating_bearing_cartridge": "SECONDARY STRUCTURAL",
    "x_fixed_bearing_cartridge": "SECONDARY STRUCTURAL",
    "x_floating_bearing_cartridge": "SECONDARY STRUCTURAL",
    "z_fixed_bearing_support": "SECONDARY STRUCTURAL",
    "z_motor_service_cartridge": "SECONDARY STRUCTURAL",
    "machine_foot_front_left": "MOUNT / INTERFACE",
    "machine_foot_front_right": "MOUNT / INTERFACE",
    "machine_foot_rear_left": "MOUNT / INTERFACE",
    "machine_foot_rear_right": "MOUNT / INTERFACE",
    "spindle_mount_concept": "MOUNT / INTERFACE",
    "electronics_mount_rail": "NON-STRUCTURAL",
}

PRIMARY_LOOP = {
    "base_front_left",
    "base_front_right",
    "base_rear_left",
    "base_rear_right",
    "base_left_side_member",
    "base_right_side_member",
    "base_y_rail_carrier_left",
    "base_y_rail_carrier_right",
    "base_center_tie",
    "gantry_tower_left",
    "gantry_tower_right",
    "gantry_beam_left",
    "gantry_beam_right",
    "x_carriage_plate",
    "z_carriage_plate",
    "spindle_mount_concept",
    "moving_bed_frame",
}

JOINT_HIGHLIGHT_NAMES = {"gantry_beam_left", "gantry_beam_right"}
REVIEW_BANNER = "PHASE 4 PRELIMINARY / REVIEW ONLY"

SUBSYSTEM = {
    "base_front_left": "base load structure",
    "base_front_right": "base load structure",
    "base_rear_left": "base load structure",
    "base_rear_right": "base load structure",
    "base_left_side_member": "base load structure",
    "base_right_side_member": "base load structure",
    "base_center_tie": "base load structure",
    "base_y_rail_carrier_left": "Y axis/base interfaces",
    "base_y_rail_carrier_right": "Y axis/base interfaces",
    "y_motor_service_pocket": "Y axis/base interfaces",
    "y_fixed_bearing_cartridge": "Y axis/base interfaces",
    "y_floating_bearing_cartridge": "Y axis/base interfaces",
    "gantry_tower_left": "fixed gantry",
    "gantry_tower_right": "fixed gantry",
    "gantry_beam_left": "fixed gantry",
    "gantry_beam_right": "fixed gantry",
    "x_fixed_bearing_cartridge": "X/Z moving structure",
    "x_floating_bearing_cartridge": "X/Z moving structure",
    "x_carriage_plate": "X/Z moving structure",
    "z_carriage_plate": "X/Z moving structure",
    "z_fixed_bearing_support": "X/Z moving structure",
    "z_motor_service_cartridge": "X/Z moving structure",
    "spindle_mount_concept": "spindle interface",
    "moving_bed_frame": "moving bed",
    "machine_foot_front_left": "mounting/accessory",
    "machine_foot_front_right": "mounting/accessory",
    "machine_foot_rear_left": "mounting/accessory",
    "machine_foot_rear_right": "mounting/accessory",
    "electronics_mount_rail": "mounting/accessory",
}

REMOVABLE = {
    "y_motor_service_pocket",
    "y_fixed_bearing_cartridge",
    "y_floating_bearing_cartridge",
    "x_fixed_bearing_cartridge",
    "x_floating_bearing_cartridge",
    "z_fixed_bearing_support",
    "z_motor_service_cartridge",
    "machine_foot_front_left",
    "machine_foot_front_right",
    "machine_foot_rear_left",
    "machine_foot_rear_right",
    "electronics_mount_rail",
    "spindle_mount_concept",
}

PRINT_BUCKET = {
    name: "closed sections"
    for name in (
        "base_front_left",
        "base_front_right",
        "base_rear_left",
        "base_rear_right",
        "base_left_side_member",
        "base_right_side_member",
        "base_center_tie",
        "gantry_tower_left",
        "gantry_tower_right",
        "gantry_beam_left",
        "gantry_beam_right",
    )
}
PRINT_BUCKET.update(
    {
        name: "ribbed plates / bed / rail carriers"
        for name in (
            "base_y_rail_carrier_left",
            "base_y_rail_carrier_right",
            "x_carriage_plate",
            "z_carriage_plate",
            "moving_bed_frame",
        )
    }
)
PRINT_BUCKET.update(
    {
        name: "local interfaces"
        for name in set(CLASSIFICATION) - set(PRINT_BUCKET)
    }
)

COLORS = {
    "CRITICAL STRUCTURAL": (194, 82, 59),
    "SECONDARY STRUCTURAL": (217, 153, 49),
    "MOUNT / INTERFACE": (80, 133, 169),
    "NON-STRUCTURAL": (128, 143, 155),
    "hardware": (168, 181, 190),
    "bed-support": (120, 145, 82),
    "pcb": (68, 153, 102),
    "ghost": (185, 194, 201),
}


@dataclass(frozen=True)
class Triangle:
    points: tuple[Vec3, Vec3, Vec3]
    color: tuple[int, int, int]
    edge: tuple[int, int, int]
    name: str
    priority: int


@dataclass(frozen=True)
class RenderItem:
    name: str
    shape: Any
    color: tuple[int, int, int]
    edge: tuple[int, int, int]
    offset: Vec3 = (0.0, 0.0, 0.0)
    priority: int = 0


def _add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _scale(a: Vec3, factor: float) -> Vec3:
    return (a[0] * factor, a[1] * factor, a[2] * factor)


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _norm(a: Vec3) -> Vec3:
    length = math.sqrt(_dot(a, a))
    return (a[0] / length, a[1] / length, a[2] / length) if length else (0.0, 0.0, 0.0)


def _shade(color: tuple[int, int, int], normal: Vec3, light: Vec3) -> tuple[int, int, int]:
    intensity = 0.34 + 0.66 * max(0.0, _dot(_norm(normal), light))
    return tuple(max(0, min(255, round(channel * intensity))) for channel in color)


def _mesh_shape(shape: Any, name: str, color: tuple[int, int, int], edge: tuple[int, int, int], priority: int) -> list[Triangle]:
    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopoDS import TopoDS
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer

    wrapped = shape.wrapped
    BRepMesh_IncrementalMesh(wrapped, 0.7, False, 0.5, True)
    explorer = TopExp_Explorer(wrapped, TopAbs_FACE)
    triangles: list[Triangle] = []
    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        triangulation = BRep_Tool.Triangulation_s(face, face.Location())
        if triangulation:
            transform = face.Location().Transformation()
            points: list[Vec3] = []
            for index in range(1, triangulation.NbNodes() + 1):
                point = triangulation.Node(index).Transformed(transform)
                points.append((float(point.X()), float(point.Y()), float(point.Z())))
            for index in range(1, triangulation.NbTriangles() + 1):
                first, second, third = triangulation.Triangle(index).Get()
                triangles.append(
                    Triangle(
                        (points[first - 1], points[second - 1], points[third - 1]),
                        color,
                        edge,
                        name,
                        priority,
                    )
                )
        explorer.Next()
    return triangles


def _is_reference_envelope(name: str) -> bool:
    return any(
        marker in name
        for marker in (
            "tool_point_travel",
            "spindle_envelope",
            "tool_envelope",
            "spindle_xy_swept_envelope",
            "swept_bed_envelope",
        )
    )


def _reference_style(name: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if "moving_bed_support" in name or "spoilboard" in name:
        return COLORS["bed-support"], (69, 84, 49)
    if "pcb_working_area" in name:
        return COLORS["pcb"], (31, 83, 53)
    return COLORS["hardware"], (76, 88, 97)


def _visible_components(model: Any, *, structural_only: bool = False) -> Iterable[Any]:
    for component in model.components:
        if structural_only and component.name not in CLASSIFICATION:
            continue
        if not structural_only and component.name.startswith("phase3a_") and _is_reference_envelope(component.name):
            continue
        yield component


def _item_for(component: Any, highlight: str = "normal", offset: Vec3 = (0.0, 0.0, 0.0)) -> RenderItem:
    name = component.name
    if name in CLASSIFICATION:
        classification = CLASSIFICATION[name]
        base = COLORS[classification]
        if highlight == "force":
            base = (230, 74, 38) if name in PRIMARY_LOOP else (157, 167, 174)
        elif highlight == "joint":
            base = (239, 87, 42) if name in JOINT_HIGHLIGHT_NAMES else (176, 185, 190)
        edge = tuple(max(0, channel - 64) for channel in base)
        return RenderItem(name, component.shape, base, edge, offset, 2 if name in PRIMARY_LOOP else 1)
    base, edge = _reference_style(name)
    return RenderItem(name, component.shape, base, edge, offset, 0)


def _project(point: Vec3, center: Vec3, right: Vec3, up: Vec3, view_dir: Vec3, scale: float, width: int, height: int) -> tuple[Vec2, float]:
    relative = _sub(point, center)
    horizontal = _dot(relative, right)
    vertical = _dot(relative, up)
    depth = _dot(relative, view_dir)
    return (width * 0.5 + horizontal * scale, height * 0.5 - vertical * scale), depth


def _view_basis(azimuth_deg: float, elevation_deg: float) -> tuple[Vec3, Vec3, Vec3]:
    azimuth = math.radians(azimuth_deg)
    elevation = math.radians(elevation_deg)
    view_dir = _norm((math.cos(azimuth) * math.cos(elevation), math.sin(azimuth) * math.cos(elevation), math.sin(elevation)))
    if abs(view_dir[2]) > 0.94:
        right = (1.0, 0.0, 0.0)
    else:
        right = _norm(_cross(view_dir, (0.0, 0.0, 1.0)))
    up = _norm(_cross(right, view_dir))
    return right, up, view_dir


def render_view(
    items: list[RenderItem],
    output: Path,
    title: str,
    azimuth_deg: float,
    elevation_deg: float,
    legend: tuple[str, ...],
    width: int = 1100,
    height: int = 820,
) -> None:
    triangles: list[Triangle] = []
    for item in items:
        for triangle in _mesh_shape(item.shape, item.name, item.color, item.edge, item.priority):
            triangles.append(
                Triangle(
                    tuple(_add(point, item.offset) for point in triangle.points),
                    triangle.color,
                    triangle.edge,
                    triangle.name,
                    triangle.priority,
                )
            )
    if not triangles:
        raise RuntimeError(f"No tessellated geometry for {title}")
    vertices = [point for triangle in triangles for point in triangle.points]
    center = (
        (min(point[0] for point in vertices) + max(point[0] for point in vertices)) * 0.5,
        (min(point[1] for point in vertices) + max(point[1] for point in vertices)) * 0.5,
        (min(point[2] for point in vertices) + max(point[2] for point in vertices)) * 0.5,
    )
    right, up, view_dir = _view_basis(azimuth_deg, elevation_deg)
    projected: list[tuple[Triangle, list[Vec2], float]] = []
    extent = 0.0
    for triangle in triangles:
        points2: list[Vec2] = []
        depths: list[float] = []
        for point in triangle.points:
            point2, depth = _project(point, center, right, up, view_dir, 1.0, width, height)
            points2.append(point2)
            depths.append(depth)
            extent = max(extent, abs(point2[0] - width * 0.5), abs(point2[1] - height * 0.5))
        projected.append((triangle, points2, sum(depths) / 3.0))
    scale = min((width * 0.42) / max(extent, 1.0), (height * 0.42) / max(extent, 1.0))
    # Re-project at the fitted scale and paint far faces first.
    fitted: list[tuple[Triangle, list[Vec2], float]] = []
    for triangle, _, _ in projected:
        points2: list[Vec2] = []
        depths: list[float] = []
        for point in triangle.points:
            point2, depth = _project(point, center, right, up, view_dir, scale, width, height)
            points2.append(point2)
            depths.append(depth)
        fitted.append((triangle, points2, sum(depths) / 3.0))
    fitted.sort(key=lambda value: (value[2], value[0].priority))

    image = Image.new("RGB", (width, height), (246, 248, 249))
    draw = ImageDraw.Draw(image)
    light = _norm((-0.35, -0.45, 0.82))
    for triangle, points2, _ in fitted:
        normal = _cross(_sub(triangle.points[1], triangle.points[0]), _sub(triangle.points[2], triangle.points[0]))
        fill = _shade(triangle.color, normal, light)
        draw.polygon(points2, fill=fill)
        if triangle.priority >= 1:
            draw.line(points2 + [points2[0]], fill=triangle.edge, width=1, joint="curve")

    draw.rectangle((18, 16, width - 18, 62), fill=(30, 42, 51))
    draw.text((32, 28), title, fill=(245, 248, 249))
    draw.text((width - 280, 29), REVIEW_BANNER, fill=(193, 205, 211))
    legend_y = height - 54
    x = 28
    for label in legend:
        if label in COLORS:
            color = COLORS[label]
        elif label == "hardware/reference":
            color = COLORS["hardware"]
        elif label == "force-loop PETG":
            color = (230, 74, 38)
        elif label == "J1 beam halves" or label == "highlighted interface":
            color = (239, 87, 42)
        else:
            color = (128, 143, 155)
        draw.rectangle((x, legend_y, x + 18, legend_y + 18), fill=color, outline=(48, 58, 64))
        draw.text((x + 25, legend_y + 2), label, fill=(39, 51, 59))
        x += 25 + max(60, len(label) * 7)
        if x > width - 200:
            legend_y -= 24
            x = 28
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def _parts_metrics(model: Any) -> list[dict[str, Any]]:
    parameters = {part.part_id: part for part in P.print_parts}
    rows: list[dict[str, Any]] = []
    for component in model.structural_parts:
        bbox = component.shape.bounding_box()
        size = tuple(round(float(getattr(bbox.size, axis)), 3) for axis in ("X", "Y", "Z"))
        volume = float(component.shape.volume)
        parameter = parameters[component.name]
        rows.append(
            {
                "part_id": component.name,
                "title": parameter.title,
                "classification": CLASSIFICATION[component.name],
                "subsystem": SUBSYSTEM[component.name],
                "quantity": 1,
                "volume_mm3": volume,
                "cad_mass_kg": volume * P.petg_density_kg_per_mm3,
                "actual_bbox_mm": size,
                "nominal_bbox_mm": parameter.nominal_bbox_mm,
                "print_orientation": parameter.print_orientation,
                "support_requirement": parameter.support_requirement,
                "brim_requirement": parameter.brim_requirement,
                "warping_risk": parameter.warping_risk,
                "layer_load_concern": parameter.layer_load_concern,
                "direct_force_loop": component.name in PRIMARY_LOOP,
                "removable_service_part": component.name in REMOVABLE,
                "print_mass_bucket": PRINT_BUCKET[component.name],
            }
        )
    return sorted(rows, key=lambda row: row["part_id"])


def build_metrics(model: Any) -> dict[str, Any]:
    rows = _parts_metrics(model)
    estimate = phase4_structural_estimate()
    class_mass: dict[str, float] = {}
    subsystem_mass: dict[str, float] = {}
    bucket_mass: dict[str, float] = {}
    for row in rows:
        class_mass[row["classification"]] = class_mass.get(row["classification"], 0.0) + row["cad_mass_kg"]
        subsystem_mass[row["subsystem"]] = subsystem_mass.get(row["subsystem"], 0.0) + row["cad_mass_kg"]
        bucket_mass[row["print_mass_bucket"]] = bucket_mass.get(row["print_mass_bucket"], 0.0) + row["cad_mass_kg"]
    expected_real_mass_kg = {
        "closed sections": (bucket_mass["closed sections"] * 0.55, bucket_mass["closed sections"] * 0.75),
        "ribbed plates / bed / rail carriers": (
            bucket_mass["ribbed plates / bed / rail carriers"] * 0.50,
            bucket_mass["ribbed plates / bed / rail carriers"] * 0.70,
        ),
        "local interfaces": (bucket_mass["local interfaces"] * 0.65, bucket_mass["local interfaces"] * 0.85),
    }
    real_low = sum(value[0] for value in expected_real_mass_kg.values())
    real_high = sum(value[1] for value in expected_real_mass_kg.values())
    return {
        "phase": "4-preliminary-structural-architecture-hardware-freeze",
        "status": "accepted-preliminary-architecture-hardware-freeze",
        "source_variant": P.reference_variant_id,
        "owner_boundary": {
            "phase4_preliminary_architecture_baseline_accepted": True,
            "phase4_manufacturing_ready": False,
            "phase5_started": False,
            "production_release": False,
        },
        "structural_part_count": len(rows),
        "critical_structural_part_count": sum(row["classification"] == "CRITICAL STRUCTURAL" for row in rows),
        "assembly_component_count": len(model.components),
        "assembly_bbox_mm": model.bounding_box_mm,
        "density_kg_per_mm3": P.petg_density_kg_per_mm3,
        "total_modeled_volume_mm3": sum(row["volume_mm3"] for row in rows),
        "cad_solid_equivalent_mass_kg": sum(row["cad_mass_kg"] for row in rows),
        "class_mass_kg": class_mass,
        "subsystem_mass_kg": subsystem_mass,
        "print_mass_bucket_cad_kg": bucket_mass,
        "conceptual_real_printed_mass_kg": {
            "low": real_low,
            "high": real_high,
            "basis": "0.55-0.75 closed sections, 0.50-0.70 ribbed plates/bed/carriers, 0.65-0.85 local interfaces; no slicer or hardware mass.",
        },
        "deflection": {
            "total_mm": estimate.total_tool_point_deflection_mm,
            "target_mm": estimate.target_mm,
            "acceptance_mm": estimate.acceptance_mm,
            "contributions": [
                {
                    "name": item.name,
                    "mm": item.displacement_mm,
                    "percent_of_total": item.displacement_mm / estimate.total_tool_point_deflection_mm * 100.0,
                    "method": item.method,
                }
                for item in estimate.contributions
            ],
        },
        "parts": rows,
    }


def _items_for_names(model: Any, names: set[str], highlight: str = "normal", offsets: dict[str, Vec3] | None = None) -> list[RenderItem]:
    offsets = offsets or {}
    return [_item_for(component, highlight, offsets.get(component.name, (0.0, 0.0, 0.0))) for component in model.components if component.name in names]


def generate_views(model: Any, output_dir: Path) -> list[str]:
    structural_names = set(CLASSIFICATION)
    visible_names = {component.name for component in _visible_components(model)}
    hardware_names = visible_names - structural_names
    all_names = structural_names | hardware_names
    views = [
        ("A", "01-complete-isometric.png", "A - Complete P2/Phase 4 review assembly - isometric", 38.0, 25.0, _items_for_names(model, all_names), ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE", "hardware/reference")),
        ("B", "02-front.png", "B - Front elevation - fixed gantry and moving bed", -90.0, 5.0, _items_for_names(model, all_names), ("CRITICAL STRUCTURAL", "hardware/reference")),
        ("C", "03-side.png", "C - Side elevation - Y screw, bed, tower and Z stack", 0.0, 5.0, _items_for_names(model, all_names), ("CRITICAL STRUCTURAL", "hardware/reference")),
        ("D", "04-top.png", "D - Top view - PCB/bed and rail spacing envelope", 0.0, 88.0, _items_for_names(model, all_names), ("CRITICAL STRUCTURAL", "bed-support", "hardware/reference")),
        (
            "E",
            "05-exploded-structural.png",
            "E - Exploded structural concept - review decomposition",
            38.0,
            25.0,
            _items_for_names(
                model,
                structural_names,
                offsets={
                    **{name: (0.0, 0.0, -42.0) for name in structural_names if name.startswith("base_") or name.startswith("machine_foot")},
                    **{name: (0.0, 0.0, 44.0) for name in structural_names if name.startswith("gantry_")},
                    **{name: (0.0, 48.0, 0.0) for name in structural_names if name.startswith(("x_", "z_", "spindle_"))},
                    "moving_bed_frame": (0.0, -45.0, 0.0),
                    "electronics_mount_rail": (0.0, 0.0, -65.0),
                },
            ),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE"),
        ),
        ("F", "06-highlighted-force-loop.png", "F - Primary force-loop PETG highlighted", 38.0, 25.0, _items_for_names(model, all_names, "force"), ("force-loop PETG", "hardware/reference")),
        (
            "G",
            "07-gantry-joint-close-up.png",
            "G - Gantry close-up - J1 split beam and tower interfaces",
            -38.0,
            25.0,
            _items_for_names(model, {"gantry_tower_left", "gantry_tower_right", "gantry_beam_left", "gantry_beam_right", "x_fixed_bearing_cartridge", "x_floating_bearing_cartridge", "phase3a_x_rail_1", "phase3a_x_rail_2", "phase3a_x_screw"}, "joint"),
            ("J1 beam halves", "highlighted interface", "hardware/reference"),
        ),
        (
            "H",
            "08-y-rail-base-close-up.png",
            "H - Y rail/base close-up - carrier, tower foot and base loop",
            -74.0,
            16.0,
            _items_for_names(model, {name for name in all_names if name.startswith(("base_", "y_", "machine_foot", "gantry_tower")) or name.startswith(("phase3a_y_rail", "phase3a_y_carriage", "phase3a_y_screw", "phase3a_y_nut", "phase3a_y_fixed", "phase3a_y_floating", "phase3a_y_coupler", "phase3a_y_nema"))}),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "hardware/reference"),
        ),
        (
            "I",
            "09-bed-underside.png",
            "I - Moving-bed underside - ribs, centered nut boss and carriages",
            35.0,
            -48.0,
            _items_for_names(model, {"moving_bed_frame", "phase3a_moving_bed_support", "phase3a_spoilboard", "phase3a_y_rail_1", "phase3a_y_rail_2", "phase3a_y_carriage_1", "phase3a_y_carriage_2", "phase3a_y_carriage_3", "phase3a_y_carriage_4", "phase3a_y_screw", "phase3a_y_nut"}),
            ("CRITICAL STRUCTURAL", "bed-support", "hardware/reference"),
        ),
        (
            "J",
            "10-z-x-close-up.png",
            "J - X/Z close-up - rail seats, moving plates and spindle mount",
            -42.0,
            22.0,
            _items_for_names(model, {name for name in all_names if name in {"x_carriage_plate", "z_carriage_plate", "z_fixed_bearing_support", "z_motor_service_cartridge", "spindle_mount_concept", "gantry_beam_left", "gantry_beam_right"} or name.startswith(("phase3a_x_rail", "phase3a_x_carriage", "phase3a_x_screw", "phase3a_z_rail", "phase3a_z_carriage", "phase3a_z_screw", "phase3a_z_nut", "phase3a_z_fixed", "phase3a_z_floating", "phase3a_z_coupler", "phase3a_z_nema", "phase3a_spindle_mount"))}),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE", "hardware/reference"),
        ),
    ]
    generated: list[str] = []
    for _, filename, title, azimuth, elevation, items, legend in views:
        render_view(items, output_dir / filename, title, azimuth, elevation, legend)
        generated.append(filename)
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs" / "architecture" / "phase-4-review",
        help="tracked review-view output directory",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    model = build_phase4_assembly()
    metrics = build_metrics(model)
    generated_views = generate_views(model, args.output_dir)
    metrics["review_views"] = generated_views
    (args.output_dir / "phase4-review-metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output_dir": str(args.output_dir), "views": generated_views, "mass_kg": metrics["cad_solid_equivalent_mass_kg"], "deflection_mm": metrics["deflection"]["total_mm"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
