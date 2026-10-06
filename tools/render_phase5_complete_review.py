"""Render lightweight review PNGs from the complete-machine STL scene.

This renderer intentionally has no CAD dependency.  It reads the local STL
scene exported by the pinned CAD runner and uses a simple orthographic
triangle painter, keeping review images reproducible even when the CAD
environment does not include a plotting library.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import struct
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]


COLORS = {
    "printed-structural": (67, 133, 185),
    "linear-guide": (150, 157, 166),
    "transmission": (197, 144, 63),
    "motor": (62, 66, 72),
    "spindle": (178, 76, 53),
    "workholding": (220, 174, 70),
    "probe": (111, 184, 157),
    "controller": (49, 143, 89),
    "limit": (212, 75, 151),
    "cable": (50, 53, 59),
    "support": (94, 96, 101),
}


def _point(values: Iterable[float]) -> Point:
    values = tuple(float(value) for value in values)
    return values[0], values[1], values[2]


def _read_stl(path: Path) -> list[Triangle]:
    data = path.read_bytes()
    triangles: list[Triangle] = []
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if 84 + count * 50 == len(data):
            offset = 84
            for _ in range(count):
                values = struct.unpack_from("<12fH", data, offset)
                triangles.append((_point(values[3:6]), _point(values[6:9]), _point(values[9:12])))
                offset += 50
            return triangles
    text = data.decode("utf-8", errors="ignore")
    vertices: list[Point] = []
    for line in text.splitlines():
        fields = line.strip().split()
        if len(fields) == 4 and fields[0].lower() == "vertex":
            vertices.append(_point(fields[1:4]))
            if len(vertices) == 3:
                triangles.append((vertices[0], vertices[1], vertices[2]))
                vertices = []
    return triangles


def _scene_from_manifest(manifest: dict, root: Path) -> list[dict]:
    scene = []
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
    x2 = x1
    y2 = y1 * math.cos(elevation) - z1 * math.sin(elevation)
    z2 = y1 * math.sin(elevation) + z1 * math.cos(elevation)
    return x2, y2, z2


def _offset_for(name: str, category: str, mode: str) -> Point:
    if mode == "none":
        return 0.0, 0.0, 0.0
    if mode == "complete":
        return 0.0, 0.0, 0.0
    if mode == "machine":
        if category == "printed-structural":
            return (0.0, 0.0, 0.0)
        if category in {"controller", "cable"}:
            return (0.0, 35.0, 35.0)
        if category in {"workholding", "probe"}:
            return (0.0, 10.0, 20.0)
        return (0.0, 0.0, 18.0)
    if mode == "base-y":
        if "base_" in name or name.startswith("machine_foot"):
            return (-35.0, 0.0, 0.0)
        if name.startswith("y_") or name.startswith("y-") or name.startswith("y_"):
            return (35.0, 0.0, 25.0)
        if name in {"moving_bed_frame", "spoilboard", "pcb_envelope"}:
            return (0.0, 30.0, 55.0)
        return 0.0, 0.0, 0.0
    if mode == "gantry-x":
        if "gantry_left" in name or name.startswith("x_") or name.startswith("x-"):
            return (-30.0, 0.0, 15.0)
        if "gantry_right" in name or name.startswith("z_") or name.startswith("spindle"):
            return (30.0, 0.0, 35.0)
        return 0.0, 0.0, 0.0
    if mode == "z-spindle":
        if name.startswith("z_") or "spindle" in name or name == "tool_envelope":
            return (35.0, 0.0, 30.0)
        if category == "linear-guide":
            return (-25.0, 0.0, 0.0)
        return 0.0, 0.0, 0.0
    return 0.0, 0.0, 0.0


def _select(scene: list[dict], names: set[str] | None) -> list[dict]:
    if names is None:
        return scene
    return [item for item in scene if item["name"] in names]


def _render(
    scene: list[dict],
    output: Path,
    *,
    title: str,
    elevation: float,
    azimuth: float,
    mode: str = "none",
    names: set[str] | None = None,
) -> None:
    selected = _select(scene, names)
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
    min_x = min(point[0] for point in all_points)
    max_x = max(point[0] for point in all_points)
    min_z = min(point[2] for point in all_points)
    max_z = max(point[2] for point in all_points)
    span = max(max_x - min_x, max_z - min_z, 1.0)
    scale = 760.0 / span
    center_x = (min_x + max_x) / 2.0
    center_z = (min_z + max_z) / 2.0

    def canvas(point: tuple[float, float]) -> tuple[float, float]:
        return (600.0 + (point[0] - center_x) * scale, 465.0 - (point[1] - center_z) * scale)

    for depth, points, color in sorted(projected, key=lambda item: item[0]):
        polygon = [canvas(point) for point in points]
        shade = max(0.62, min(1.12, 0.86 + depth / max(span * 2.0, 1.0)))
        shaded = tuple(max(0, min(255, int(channel * shade))) for channel in color)
        draw.polygon(polygon, fill=shaded, outline=(45, 50, 55))
    draw.rectangle((20, 20, 1180, 880), outline=(120, 128, 136), width=2)
    draw.text((42, 38), title, fill=(25, 30, 35))
    draw.text((42, 62), "Phase 5 virtual manufacturing-CAD review | geometry and envelopes are provisional", fill=(65, 70, 75))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def render(manifest_path: Path, output_dir: Path) -> list[Path]:
    manifest_path = manifest_path.resolve()
    root = Path.cwd().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    scene = _scene_from_manifest(manifest, root)
    names = {item["name"] for item in scene}
    focus_base = {name for name in names if name.startswith(("base_", "y_", "machine_foot", "moving_bed", "spoilboard", "pcb_", "workholding", "conductive_probe", "probe_"))}
    focus_gantry = {name for name in names if name.startswith(("gantry_", "x_", "z_", "spindle", "tool_"))}
    focus_z = {name for name in names if name.startswith(("z_", "spindle", "tool_", "x_z_backbone", "x_carriage"))}
    focus_electronics = {name for name in names if name.startswith(("arduino", "cnc_", "driver_", "controller_", "motor_cable", "x_home", "y_home", "z_home", "electronics_"))}
    focus_pcb = {name for name in names if name in {"moving_bed_frame", "spoilboard", "pcb_envelope", "conductive_probe", "probe_cable_route", "workholding_clamp_front", "workholding_clamp_rear", "workholding_clamp_right", "tool_envelope"}}
    views = (
        ("01-complete-front-isometric.png", "Complete machine — front isometric", 28.0, -50.0, "complete", None),
        ("02-complete-rear-isometric.png", "Complete machine — rear isometric", 28.0, 130.0, "complete", None),
        ("03-top.png", "Complete machine — top", 88.0, -90.0, "none", None),
        ("04-front.png", "Complete machine — front", 8.0, -90.0, "none", None),
        ("05-side.png", "Complete machine — side", 8.0, 0.0, "none", None),
        ("06-exploded-machine.png", "Complete machine — exploded review", 28.0, -50.0, "machine", None),
        ("07-exploded-base-y.png", "Base, Y motion and workholding — exploded", 30.0, -50.0, "base-y", focus_base),
        ("08-exploded-gantry-x.png", "Gantry and X motion — exploded", 28.0, -50.0, "gantry-x", focus_gantry),
        ("09-exploded-z-spindle.png", "Z and spindle — exploded", 22.0, -50.0, "z-spindle", focus_z),
        ("10-electronics-cable.png", "Controller, limits and cable service", 28.0, -50.0, "none", focus_electronics),
        ("11-pcb-workholding.png", "PCB, spoilboard, probe and workholding", 35.0, -50.0, "none", focus_pcb),
        ("12-motion-envelope.png", "Motion envelope and tool access", 28.0, -50.0, "none", {name for name in names if name in {"spindle_envelope", "tool_envelope", "pcb_envelope", "spoilboard", "moving_bed_frame", "x_rail_lower", "x_rail_upper", "y_rail_left", "y_rail_right", "z_rail_left", "z_rail_right"}}),
    )
    outputs: list[Path] = []
    for filename, title, elevation, azimuth, mode, selected in views:
        path = output_dir / filename
        _render(scene, path, title=title, elevation=elevation, azimuth=azimuth, mode=mode, names=selected)
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
