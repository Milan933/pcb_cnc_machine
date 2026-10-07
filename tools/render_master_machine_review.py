"""Render the master-assembly review package from manifest scene STL files."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import struct
from typing import Iterable

from PIL import Image, ImageDraw


Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]

COLORS = {
    "printed-structural": (54, 128, 185),
    "linear-guide": (145, 153, 164),
    "transmission": (194, 139, 48),
    "motor": (58, 63, 71),
    "spindle": (181, 75, 47),
    "workholding": (219, 168, 54),
    "probe": (70, 168, 142),
    "controller": (42, 143, 83),
    "limit": (207, 72, 147),
    "cable-management": (41, 48, 56),
    "fastener": (205, 205, 205),
}


def _point(values: Iterable[float]) -> Point:
    values = tuple(float(value) for value in values)
    return values[0], values[1], values[2]


def _read_stl(path: Path) -> list[Triangle]:
    data = path.read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if 84 + count * 50 == len(data):
            triangles: list[Triangle] = []
            offset = 84
            for _ in range(count):
                values = struct.unpack_from("<12fH", data, offset)
                triangles.append((_point(values[3:6]), _point(values[6:9]), _point(values[9:12])))
                offset += 50
            return triangles
    text = data.decode("utf-8", errors="ignore")
    vertices: list[Point] = []
    triangles = []
    for line in text.splitlines():
        fields = line.strip().split()
        if len(fields) == 4 and fields[0].lower() == "vertex":
            vertices.append(_point(fields[1:4]))
            if len(vertices) == 3:
                triangles.append((vertices[0], vertices[1], vertices[2]))
                vertices = []
    return triangles


def _scene_from_manifest(manifest: dict, root: Path) -> list[dict]:
    scene: list[dict] = []
    for item in manifest["scene_components"]:
        path = Path(item["stl"])
        if not path.is_absolute():
            path = root / path
        triangles = _read_stl(path)
        if triangles:
            scene.append({**item, "triangles": triangles})
    return scene


def _rotate(point: Point, elevation_deg: float, azimuth_deg: float) -> tuple[float, float, float]:
    x, y, z = point
    azimuth = math.radians(azimuth_deg)
    elevation = math.radians(elevation_deg)
    x1 = x * math.cos(azimuth) - y * math.sin(azimuth)
    y1 = x * math.sin(azimuth) + y * math.cos(azimuth)
    z1 = z
    return x1, y1 * math.cos(elevation) - z1 * math.sin(elevation), y1 * math.sin(elevation) + z1 * math.cos(elevation)


def _offset_for(name: str, category: str, mode: str) -> Point:
    if mode in {"complete", "none"}:
        return 0.0, 0.0, 0.0
    if mode == "exploded":
        if category == "printed-structural":
            return 0.0, 0.0, 0.0
        if category in {"controller", "cable-management"}:
            return 0.0, 42.0, 34.0
        if category in {"workholding", "probe"}:
            return 0.0, 12.0, 24.0
        return 0.0, 0.0, 20.0
    if mode == "base-y":
        if name.startswith(("base_", "machine_foot", "y_", "moving_bed", "spoilboard", "pcb_", "workholding", "conductive", "probe")):
            return (-30.0, 0.0, 18.0) if name.startswith("base_") else (30.0, 0.0, 28.0)
    if mode == "gantry-x":
        if name.startswith(("gantry_", "x_")):
            return (-24.0, 0.0, 18.0) if "left" in name or "fixed" in name else (24.0, 0.0, 30.0)
    if mode == "z-spindle":
        if name.startswith(("z_", "spindle", "tool_")):
            return 30.0, 0.0, 28.0
        if category == "linear-guide":
            return -22.0, 0.0, 0.0
    if mode == "electronics":
        if category == "printed-structural":
            return 0.0, 0.0, -12.0
        return 0.0, 20.0, 20.0
    return 0.0, 0.0, 0.0


def _select(scene: list[dict], names: set[str] | None = None, categories: set[str] | None = None) -> list[dict]:
    result = scene
    if names is not None:
        result = [item for item in result if item["name"] in names]
    if categories is not None:
        result = [item for item in result if item["category"] in categories]
    return result


def _render(scene: list[dict], output: Path, *, title: str, elevation: float, azimuth: float, mode: str, names: set[str] | None = None, categories: set[str] | None = None) -> None:
    selected = _select(scene, names, categories)
    projected: list[tuple[float, list[tuple[float, float]], tuple[int, int, int]]] = []
    all_points: list[tuple[float, float, float]] = []
    for item in selected:
        dx, dy, dz = _offset_for(item["name"], item["category"], mode)
        color = COLORS.get(item["category"], (120, 120, 120))
        for triangle in item["triangles"]:
            rotated = [_rotate((point[0] + dx, point[1] + dy, point[2] + dz), elevation, azimuth) for point in triangle]
            all_points.extend(rotated)
            projected.append((sum(point[1] for point in rotated) / 3.0, [(point[0], point[2]) for point in rotated], color))
    image = Image.new("RGB", (1200, 900), (245, 247, 249))
    draw = ImageDraw.Draw(image)
    if not all_points:
        draw.text((40, 40), "No scene triangles", fill=(30, 30, 30))
        image.save(output)
        return
    min_x, max_x = min(point[0] for point in all_points), max(point[0] for point in all_points)
    min_z, max_z = min(point[2] for point in all_points), max(point[2] for point in all_points)
    span = max(max_x - min_x, max_z - min_z, 1.0)
    scale = 760.0 / span
    center_x, center_z = (min_x + max_x) / 2.0, (min_z + max_z) / 2.0

    def canvas(point: tuple[float, float]) -> tuple[float, float]:
        return 600.0 + (point[0] - center_x) * scale, 465.0 - (point[1] - center_z) * scale

    for depth, points, color in sorted(projected, key=lambda item: item[0]):
        polygon = [canvas(point) for point in points]
        shade = max(0.62, min(1.12, 0.86 + depth / max(span * 2.0, 1.0)))
        shaded = tuple(max(0, min(255, int(channel * shade))) for channel in color)
        draw.polygon(polygon, fill=shaded, outline=(45, 50, 55))
    draw.rectangle((20, 20, 1180, 880), outline=(120, 128, 136), width=2)
    draw.text((42, 38), title, fill=(25, 30, 35))
    draw.text((42, 62), "Phase 5 master-assembly review | reference hardware and PETG fit remain provisional", fill=(65, 70, 75))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def render(manifest_path: Path, output_dir: Path) -> list[Path]:
    manifest_path = manifest_path.resolve()
    root = Path.cwd().resolve()
    scene = _scene_from_manifest(json.loads(manifest_path.read_text(encoding="utf-8")), root)
    names = {item["name"] for item in scene}
    base_y = {name for name in names if name.startswith(("base_", "y_", "machine_foot", "moving_bed", "spoilboard", "pcb_", "workholding", "conductive_probe"))}
    gantry_x = {name for name in names if name.startswith(("gantry_", "x_")) or name == "spindle_5045_ac_er11"}
    z_spindle = {name for name in names if name.startswith(("z_", "spindle", "tool_")) or name == "x_z_backbone"}
    electronics = {name for name in names if name.startswith(("arduino", "cnc_", "driver_", "controller_", "x_home", "y_home", "z_home")) or "cable" in name or name == "electronics_mount_rail"}
    workholding = {name for name in names if name in {"moving_bed_frame", "spoilboard", "pcb_envelope", "conductive_probe", "workholding_clamp_front", "workholding_clamp_rear", "workholding_clamp_right", "tool_envelope"}}
    motion = {name for name in names if name in {"spindle_5045_ac_er11", "tool_envelope", "moving_bed_frame", "x_rail_lower", "x_rail_upper", "y_rail_left", "y_rail_right", "z_rail_left", "z_rail_right"}}
    views = (
        ("01-master-front-isometric.png", "Master machine - front isometric", 28.0, -50.0, "complete", None, None),
        ("02-master-rear-isometric.png", "Master machine - rear isometric", 28.0, 130.0, "complete", None, None),
        ("03-left-side.png", "Master machine - left side", 8.0, 0.0, "none", None, None),
        ("04-right-side.png", "Master machine - right side", 8.0, 180.0, "none", None, None),
        ("05-top.png", "Master machine - top", 88.0, -90.0, "none", None, None),
        ("06-front.png", "Master machine - front", 8.0, -90.0, "none", None, None),
        ("07-rear.png", "Master machine - rear", 8.0, 90.0, "none", None, None),
        ("08-base-y-detail.png", "Base and Y motion detail", 30.0, -50.0, "base-y", base_y, None),
        ("09-gantry-x-detail.png", "Gantry and X motion detail", 28.0, -50.0, "gantry-x", gantry_x, None),
        ("10-xz-spindle-detail.png", "X, Z, and spindle detail", 22.0, -50.0, "z-spindle", z_spindle, None),
        ("11-electronics-detail.png", "Controller, limits, and cable service", 28.0, -50.0, "electronics", electronics, None),
        ("12-workholding-detail.png", "PCB, spoilboard, probe, and workholding", 35.0, -50.0, "none", workholding, None),
        ("13-exploded-assembly.png", "Exploded master assembly", 28.0, -50.0, "exploded", None, None),
        ("14-printed-parts-only.png", "Derived printed-parts-only assembly", 28.0, -50.0, "none", None, {"printed-structural"}),
        ("15-hardware-only.png", "Hardware-only master assembly", 28.0, -50.0, "none", None, {"linear-guide", "transmission", "motor", "spindle", "workholding", "probe", "controller", "limit", "cable-management", "fastener"}),
        ("16-motion-extremes.png", "Motion extremes and tool access", 28.0, -50.0, "none", motion, None),
    )
    outputs: list[Path] = []
    for filename, title, elevation, azimuth, mode, selected_names, categories in views:
        path = output_dir / filename
        _render(scene, path, title=title, elevation=elevation, azimuth=azimuth, mode=mode, names=selected_names, categories=categories)
        outputs.append(path)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outputs = render(args.manifest, args.output_dir)
    print(json.dumps({"images": [path.as_posix() for path in outputs]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
