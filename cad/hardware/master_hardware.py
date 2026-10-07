"""Dimensionally credible hardware references for the master assembly.

The shapes in this module are local derived reference/envelope models.  They
are not blind copies of downloaded third-party CAD.  Each entry in
``HARDWARE_MODEL_REGISTER`` records the public source, reuse status, and
confidence so the assembly can use a real mechanical relationship without
turning an unmeasured supplier part into a manufacturing fact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from cad.parameters import PHASE5_MASTER_PARAMETERS


@dataclass(frozen=True)
class HardwareModelSpec:
    """Traceability record for one hardware representation."""

    component: str
    manufacturer: str
    model_or_class: str
    source_url: str
    source_type: str
    license_reuse_status: str
    expected_dimensions_mm: str
    measured_model_dimensions_mm: str
    independently_verified: bool
    confidence: str
    classification: str
    repository_action: str
    notes: str


HARDWARE_MODEL_REGISTER: tuple[HardwareModelSpec, ...] = (
    HardwareModelSpec(
        "MGN12 rail and MGN12H carriage",
        "HIWIN",
        "MG series MGN12H",
        "https://hiwin-linearmotion.com/images/products/linear-guide/mg-series/mg.pdf",
        "official manufacturer dimensional catalog",
        "No third-party CAD copied; local derived model is publishable project geometry",
        "MGN12 rail section 12 x 8; MGN12H carriage 27 x 13 x 45.4; 25 mm nominal rail pitch",
        "12 x 8 rail section and 27 x 13 x 45.4 carriage envelope",
        False,
        "high reference confidence",
        "REFERENCE-CAD",
        "Commit local derived interface/envelope only; measure owner's rail before release",
        "Official dimensions drive rail and carriage placement, not final PETG fit tolerance.",
    ),
    HardwareModelSpec(
        "MGN9 rail and MGN9H carriage",
        "HIWIN",
        "MG series MGN09H",
        "https://hiwin-linearmotion.com/images/products/linear-guide/mg-series/mg.pdf",
        "official manufacturer dimensional catalog",
        "No third-party CAD copied; local derived model is publishable project geometry",
        "MGN9 rail nominal 9 mm class; MGN9H carriage approximately 20 x 10 x 39.9",
        "9 x 6 rail envelope and 20 x 10 x 39.9 carriage envelope",
        False,
        "high reference confidence",
        "REFERENCE-CAD",
        "Commit local derived interface/envelope only; verify actual rail family",
        "The exact MGN9 variant and preload remain unresolved.",
    ),
    HardwareModelSpec(
        "T8 X/Y lead screw",
        "Unselected supplier",
        "T8 x 4 envelope",
        "",
        "project motion requirement; no supplier selected",
        "No external model acquired",
        "8 mm nominal screw diameter; 4 mm lead; end journals and nut interface vary by supplier",
        "8 mm nominal threaded envelope with 7 mm journal screening",
        False,
        "medium envelope confidence",
        "ENVELOPE-ONLY",
        "Keep local parametric envelope; measure the purchased screw and nut",
        "The thread is intentionally not modeled helically.",
    ),
    HardwareModelSpec(
        "T8 Z lead screw",
        "Unselected supplier",
        "T8 x 2 envelope",
        "",
        "project motion requirement; no supplier selected",
        "No external model acquired",
        "8 mm nominal screw diameter; 2 mm lead; end journals and nut interface vary by supplier",
        "8 mm nominal threaded envelope with 7 mm journal screening",
        False,
        "medium envelope confidence",
        "ENVELOPE-ONLY",
        "Keep local parametric envelope; measure the purchased screw and nut",
        "The Z transmission remains an interface candidate, not a purchased-part claim.",
    ),
    HardwareModelSpec(
        "T8 anti-backlash nuts",
        "Unselected supplier",
        "T8 x 4 / T8 x 2 preload nut candidates",
        "",
        "architecture candidate",
        "No external model acquired",
        "Flange, spring/preload stack, bolt spacing, and body length are supplier-specific",
        "Local 24 x 24 x 24 body plus 40 x 30 flange screening envelope",
        False,
        "low reference confidence",
        "PROVISIONAL",
        "Do not publish a supplier-specific fit; measure candidate nuts",
        "The nut architecture is represented for support and clearance only.",
    ),
    HardwareModelSpec(
        "608 fixed/floating bearing reference",
        "SKF",
        "608-2RSH / 608 class",
        "https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-608-2RSH",
        "official manufacturer catalog dimensions",
        "Local derived ring model is publishable; no SKF CAD redistributed",
        "8 mm bore x 22 mm outside diameter x 7 mm width",
        "8 x 22 x 7 mm annular envelope",
        False,
        "high reference confidence",
        "REFERENCE-CAD",
        "Commit local envelope; identify the actual fixed/floating bearing stack",
        "The assembly uses paired fixed-end and single floating-end arrangements.",
    ),
    HardwareModelSpec(
        "5 mm to 8 mm flexible coupler",
        "MISUMI reference family",
        "slit/flexible coupling, 5 x 8 bore class",
        "https://my.c.misumi-ec.com/book/MYS_EconomySeries_e-promobook202308/files/basic-html/page239.html",
        "official distributor catalog",
        "No catalog CAD copied; local dimensional envelope only",
        "Representative 20 mm outside diameter and 30 mm length; 5/8 mm bores",
        "20 x 30 mm two-bore envelope",
        False,
        "medium reference confidence",
        "REFERENCE-CAD",
        "Keep as interface envelope until a coupler is selected and measured",
        "Set-screw access and axial float must be checked against the actual coupler.",
    ),
    HardwareModelSpec(
        "owner-stock NEMA17 motor",
        "Owner stock / unselected manufacturers",
        "42.3 mm NEMA17 class",
        "",
        "owner requirement and common 3D-printer interface",
        "Local generic model; no third-party CAD copied",
        "42.3 mm frame; approximately 31 mm mounting pitch; 5 mm shaft; 40-48 mm body",
        "42.3 x 42.3 x 46 mm screening body with 5 x 20 mm shaft",
        False,
        "high interface confidence; low motor-performance confidence",
        "ENVELOPE-ONLY",
        "OWNER-SUPPLIED — DO NOT BUY; commit generic interface only and characterize stock before assignment",
        "The exact body length, current, connector, and torque class remain open.",
    ),
    HardwareModelSpec(
        "Arduino Mega 2560 controller",
        "Arduino",
        "Mega 2560 Rev3",
        "https://docs.arduino.cc/resources/datasheets/A000067-datasheet.pdf",
        "official manufacturer mechanical drawing and datasheet",
        "Official open hardware reference; local derived envelope is publishable",
        "PCB approximately 101.52 x 53.3 x 1.6 mm; USB/power/header clearance required",
        "101.52 x 53.3 x 15 mm component envelope with mounting-hole screening",
        False,
        "high reference confidence",
        "REFERENCE-CAD",
        "Commit local derived envelope; owner board variant and connector stack still need measurement",
        "The controller platform is owner-supplied and must not be replaced by assumption.",
    ),
    HardwareModelSpec(
        "owner CNC Shield",
        "Owner hardware / revision unknown",
        "Mega-compatible CNC Shield provisional envelope",
        "",
        "owner hardware identification pending",
        "No external model claimed or copied",
        "Exact shield revision, driver modules, terminals, I/O, and mounting pattern unknown",
        "100 x 60 x 18 mm provisional board/component envelope with flexible slots",
        False,
        "low reference confidence",
        "PROVISIONAL",
        "OWNER-SUPPLIED — DO NOT REPLACE absent a validated limitation; identify and measure the actual board",
        "No exact shield model is pretended.",
    ),
    HardwareModelSpec(
        "ER11 spindle candidate",
        "SycoTec",
        "5045 AC-ER11, reference 2002 5400",
        "https://sycotec.eu/en/product/5045-ac-er11/",
        "official manufacturer product page with downloadable STEP and datasheet",
        "Downloaded third-party STEP is not committed; reuse permission is not established",
        "45 mm housing; ER11 up to 8 mm; 1.6 kg; 6,000-60,000 rpm; axial length to be checked from CAD",
        "45 mm diameter x 140 mm local provisional axial envelope",
        False,
        "high candidate confidence; medium envelope-length confidence",
        "REFERENCE-CAD",
        "Keep official CAD external; publish local derived envelope only",
        "This is the realistic candidate represented in the master assembly.",
    ),
    HardwareModelSpec(
        "limit switch",
        "Omron",
        "D2F lever/pin family",
        "https://omronfs.omron.com/en_US/ecb/products/pdf/en-d2f.pdf",
        "official manufacturer dimensional datasheet",
        "Local derived envelope only; no third-party CAD redistributed",
        "Approximately 12.8 x 6.5 x 5.8 mm body; 2 mm mounting holes; lever/plunger envelope",
        "12.8 x 13 x 8 mm switch and actuation envelope",
        False,
        "high reference confidence for family envelope",
        "REFERENCE-CAD",
        "Commit local envelope; identify actual switch and connector termination",
        "The actuation geometry is modeled so homing support is not decorative.",
    ),
    HardwareModelSpec(
        "conductive tool probe",
        "Unselected supplier",
        "conductive touch plate/probe concept",
        "",
        "project process concept",
        "Local project geometry",
        "Electrical/tool contact and cable access are process-dependent",
        "25 x 25 x 2 mm touch plate plus bracket/cable access envelope",
        False,
        "low reference confidence",
        "PROVISIONAL",
        "Commit local process envelope; identify actual probe hardware and circuit",
        "Probe access is included without claiming a selected electrical device.",
    ),
)


def hardware_model_register_dicts() -> list[dict[str, Any]]:
    """Return JSON-ready source-register records."""

    return [asdict(item) for item in HARDWARE_MODEL_REGISTER]


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - CAD runner only
        raise RuntimeError("Master hardware geometry requires build123d.") from exc
    return build123d


def _box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], label: str) -> Any:
    shape = bd.Box(*size, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)).located(bd.Location(minimum))
    shape.label = label
    return shape


def _cylinder_axis(
    bd: Any,
    radius: float,
    length: float,
    start: tuple[float, float, float],
    axis: str,
    label: str,
) -> Any:
    rotations = {"x": (0.0, 90.0, 0.0), "y": (-90.0, 0.0, 0.0), "z": (0.0, 0.0, 0.0)}
    if axis not in rotations:
        raise ValueError(f"Unsupported axis {axis!r}")
    shape = bd.Cylinder(
        radius,
        length,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ).located(bd.Location(start, rotations[axis]))
    shape.label = label
    return shape


def _fuse_all(shapes: list[Any]) -> Any:
    result = shapes[0]
    for shape in shapes[1:]:
        result = result.fuse(shape)
    return result


def _axis_start(start: tuple[float, float, float], axis: str, delta: float) -> tuple[float, float, float]:
    values = list(start)
    values[{"x": 0, "y": 1, "z": 2}[axis]] += delta
    return tuple(values)


def build_mgn_rail(axis: str, length_mm: float, *, size: int = 12, label: str = "mgn_rail") -> Any:
    """Build a rail section with a documented hole-pitch screening pattern."""

    bd = _build123d()
    width, height, pitch, hole_diameter = ((12.0, 8.0, 25.0, 3.5) if size == 12 else (9.0, 6.0, 20.0, 3.2))
    if axis == "x":
        shape = _box(bd, (length_mm, width, height), (0.0, 0.0, 0.0), label)
        count = max(1, int((length_mm - 20.0) // pitch) + 1)
        for index in range(count):
            x = 10.0 + index * pitch
            if x > length_mm - 10.0:
                break
            shape = shape.cut(_cylinder_axis(bd, hole_diameter / 2.0, height + 2.0, (x, width / 2.0, -1.0), "z", f"{label}_hole_{index}"))
    elif axis == "y":
        shape = _box(bd, (width, length_mm, height), (0.0, 0.0, 0.0), label)
        count = max(1, int((length_mm - 20.0) // pitch) + 1)
        for index in range(count):
            y = 10.0 + index * pitch
            if y > length_mm - 10.0:
                break
            shape = shape.cut(_cylinder_axis(bd, hole_diameter / 2.0, height + 2.0, (width / 2.0, y, -1.0), "z", f"{label}_hole_{index}"))
    elif axis == "z":
        shape = _box(bd, (width, height, length_mm), (0.0, 0.0, 0.0), label)
        count = max(1, int((length_mm - 20.0) // pitch) + 1)
        for index in range(count):
            z = 10.0 + index * pitch
            if z > length_mm - 10.0:
                break
            shape = shape.cut(_cylinder_axis(bd, hole_diameter / 2.0, height + 2.0, (width / 2.0, -1.0, z), "y", f"{label}_hole_{index}"))
    else:
        raise ValueError(f"Unsupported rail axis {axis!r}")
    shape.label = label
    return shape


def build_mgn_carriage(axis: str, *, size: int = 12, label: str = "mgn_carriage") -> Any:
    """Build an MGN-H carriage envelope with mounting-hole clearance."""

    bd = _build123d()
    if size == 12:
        block_length, block_width, block_height, hole_spacing = 45.4, 27.0, 13.0, 20.0
    else:
        block_length, block_width, block_height, hole_spacing = 39.9, 20.0, 10.0, 15.0
    if axis in {"x", "y"}:
        long_size = (block_length, block_width, block_height) if axis == "x" else (block_width, block_length, block_height)
        shape = _box(bd, long_size, (0.0, 0.0, 0.0), label)
        x_positions = (block_length / 2.0 - hole_spacing / 2.0, block_length / 2.0 + hole_spacing / 2.0) if axis == "x" else (block_width / 2.0,)
        y_positions = (block_width / 2.0 - 7.0, block_width / 2.0 + 7.0) if axis == "x" else (block_length / 2.0 - hole_spacing / 2.0, block_length / 2.0 + hole_spacing / 2.0)
        for x in x_positions:
            for y in y_positions:
                shape = shape.cut(_cylinder_axis(bd, 1.75, block_height + 2.0, (x, y, -1.0), "z", f"{label}_hole"))
    elif axis == "z":
        shape = _box(bd, (block_width, block_height, block_length), (0.0, 0.0, 0.0), label)
        for x in (block_width / 2.0 - 5.0, block_width / 2.0 + 5.0):
            for z in (block_length / 2.0 - hole_spacing / 2.0, block_length / 2.0 + hole_spacing / 2.0):
                shape = shape.cut(_cylinder_axis(bd, 1.6, block_height + 2.0, (x, -1.0, z), "y", f"{label}_hole"))
    else:
        raise ValueError(f"Unsupported carriage axis {axis!r}")
    shape.label = label
    return shape


def build_t8_screw(axis: str, length_mm: float, lead_mm: float, *, label: str = "t8_screw") -> Any:
    """Build a non-helical T8 screw with journals and usable threaded region."""

    bd = _build123d()
    journal = PHASE5_MASTER_PARAMETERS.screw_journal_diameter_mm / 2.0
    thread = PHASE5_MASTER_PARAMETERS.screw_nominal_diameter_mm / 2.0
    journal_length = 15.0
    start = (0.0, 0.0, 0.0)
    result = _cylinder_axis(bd, thread, length_mm, start, axis, label)
    result = result.fuse(_cylinder_axis(bd, journal, journal_length, _axis_start(start, axis, -journal_length), axis, f"{label}_drive_journal"))
    result = result.fuse(_cylinder_axis(bd, journal, journal_length, _axis_start(start, axis, length_mm), axis, f"{label}_far_journal"))
    result.label = label
    return result


def build_t8_nut(*, label: str = "t8_anti_backlash_nut") -> Any:
    bd = _build123d()
    body = _box(bd, (24.0, 24.0, 24.0), (0.0, 0.0, 0.0), f"{label}_body")
    flange = _box(bd, (40.0, 30.0, 6.0), (-8.0, -3.0, 9.0), f"{label}_flange")
    bore = _cylinder_axis(bd, 4.5, 32.0, (12.0, 12.0, -1.0), "z", f"{label}_bore")
    result = _fuse_all([body, flange]).cut(bore)
    result.label = label
    return result


def build_608_bearing(axis: str, *, label: str = "bearing_608") -> Any:
    bd = _build123d()
    p = PHASE5_MASTER_PARAMETERS
    outer = _cylinder_axis(bd, p.bearing_outer_diameter_mm / 2.0, p.bearing_width_mm, (0.0, 0.0, 0.0), axis, label)
    bore = _cylinder_axis(bd, p.bearing_bore_mm / 2.0, p.bearing_width_mm + 2.0, _axis_start((0.0, 0.0, 0.0), axis, -1.0), axis, f"{label}_bore")
    result = outer.cut(bore)
    result.label = label
    return result


def build_flexible_coupler(axis: str, *, label: str = "flexible_coupler") -> Any:
    bd = _build123d()
    p = PHASE5_MASTER_PARAMETERS
    first = _cylinder_axis(bd, p.coupler_outer_diameter_mm / 2.0, p.coupler_length_mm / 2.0, (0.0, 0.0, 0.0), axis, f"{label}_motor_half")
    second = _cylinder_axis(bd, p.coupler_outer_diameter_mm / 2.0, p.coupler_length_mm / 2.0, _axis_start((0.0, 0.0, 0.0), axis, p.coupler_length_mm / 2.0), axis, f"{label}_screw_half")
    motor_bore = _cylinder_axis(bd, p.coupler_motor_bore_mm / 2.0, p.coupler_length_mm / 2.0 + 2.0, _axis_start((0.0, 0.0, 0.0), axis, -1.0), axis, f"{label}_motor_bore")
    screw_bore = _cylinder_axis(bd, p.coupler_screw_bore_mm / 2.0, p.coupler_length_mm / 2.0 + 2.0, _axis_start((0.0, 0.0, 0.0), axis, p.coupler_length_mm / 2.0 - 1.0), axis, f"{label}_screw_bore")
    result = first.cut(motor_bore).fuse(second.cut(screw_bore))
    result.label = label
    return result


def build_nema17(axis: str, *, body_length_mm: float = 46.0, label: str = "nema17") -> Any:
    """Build a generic owner-stock NEMA17 interface model."""

    bd = _build123d()
    p = PHASE5_MASTER_PARAMETERS
    half = p.nema17_frame_mm / 2.0
    body = _box(bd, (p.nema17_frame_mm, p.nema17_frame_mm, body_length_mm), (-half, -half, 0.0), f"{label}_body")
    face = _box(bd, (p.nema17_frame_mm, p.nema17_frame_mm, 3.0), (-half, -half, body_length_mm), f"{label}_face")
    pilot = _cylinder_axis(bd, 11.0, 3.0, (0.0, 0.0, body_length_mm + 3.0), "z", f"{label}_pilot")
    shaft = _cylinder_axis(bd, p.nema17_shaft_diameter_mm / 2.0, p.nema17_shaft_projection_mm, (0.0, 0.0, body_length_mm + 6.0), "z", f"{label}_shaft")
    connector = _box(bd, (12.0, 8.0, 8.0), (-6.0, -half - 5.0, body_length_mm / 2.0), f"{label}_connector")
    local = _fuse_all([body, face, pilot, shaft, connector])
    rotations = {"x": (0.0, 90.0, 0.0), "y": (-90.0, 0.0, 0.0), "z": (0.0, 0.0, 0.0)}
    if axis not in rotations:
        raise ValueError(f"Unsupported motor axis {axis!r}")
    result = local.located(bd.Location((0.0, 0.0, 0.0), rotations[axis]))
    result.label = label
    return result


def build_arduino_mega(*, label: str = "arduino_mega") -> Any:
    bd = _build123d()
    width, depth, thickness = PHASE5_MASTER_PARAMETERS.arduino_mega_board_mm
    board = _box(bd, (width, depth, thickness), (0.0, 0.0, 0.0), label)
    # Three mounting holes are represented from the official board drawing;
    # connector and header envelopes are fused into the board model.
    for index, (x, y) in enumerate(((3.2, 3.2), (3.2, depth - 3.2), (width - 3.2, depth - 3.2)), start=1):
        board = board.cut(_cylinder_axis(bd, 1.6, thickness + 2.0, (x, y, -1.0), "z", f"{label}_mount_{index}"))
    usb = _box(bd, (16.0, 16.0, 12.0), (width - 16.0, 5.0, thickness), f"{label}_usb")
    power = _box(bd, (10.0, 12.0, 10.0), (width - 12.0, depth - 14.0, thickness), f"{label}_power")
    headers = _box(bd, (width - 8.0, 5.0, 12.0), (4.0, -2.0, thickness), f"{label}_headers")
    components = _box(bd, (55.0, 30.0, 8.0), (20.0, 12.0, thickness), f"{label}_component_height")
    result = _fuse_all([board, usb, power, headers, components])
    result.label = label
    return result


def build_cnc_shield(*, label: str = "cnc_shield") -> Any:
    bd = _build123d()
    width, depth, height = PHASE5_MASTER_PARAMETERS.cnc_shield_provisional_board_mm
    board = _box(bd, (width, depth, 2.0), (0.0, 0.0, 0.0), label)
    sockets = [_box(bd, (18.0, 22.0, 12.0), (8.0 + index * 28.0, 8.0, 2.0), f"{label}_driver_{index}") for index in range(3)]
    terminals = _box(bd, (18.0, depth - 12.0, 10.0), (width - 24.0, 6.0, 2.0), f"{label}_terminals")
    usb_clearance = _box(bd, (24.0, 14.0, 12.0), (-4.0, 5.0, 2.0), f"{label}_clearance")
    result = _fuse_all([board, *sockets, terminals, usb_clearance])
    result.label = label
    return result


def build_spindle_candidate(*, label: str = "spindle_5045_ac_er11") -> Any:
    bd = _build123d()
    p = PHASE5_MASTER_PARAMETERS
    body = _cylinder_axis(bd, p.spindle_candidate_diameter_mm / 2.0, p.spindle_candidate_length_mm, (0.0, 0.0, 0.0), "z", label)
    nose = _cylinder_axis(bd, 8.0, 14.0, (0.0, 0.0, -14.0), "z", f"{label}_er11_nose")
    connector = _box(bd, (16.0, 12.0, 12.0), (-8.0, -p.spindle_candidate_diameter_mm / 2.0 - 8.0, p.spindle_candidate_length_mm - 18.0), f"{label}_connector")
    result = _fuse_all([body, nose, connector])
    result.label = label
    return result


def build_d2f_limit_switch(*, label: str = "limit_switch") -> Any:
    bd = _build123d()
    body = _box(bd, (12.8, 6.5, 5.8), (0.0, 0.0, 0.0), label)
    lever = _box(bd, (13.0, 1.5, 0.8), (8.0, 2.5, 5.0), f"{label}_lever")
    result = _fuse_all([body, lever])
    for x in (2.0, 10.8):
        result = result.cut(_cylinder_axis(bd, 1.0, 7.0, (x, -0.25, 3.0), "y", f"{label}_mount"))
    result.label = label
    return result


def build_conductive_probe(*, label: str = "conductive_probe") -> Any:
    bd = _build123d()
    plate = _box(bd, (25.0, 25.0, 2.0), (0.0, 0.0, 0.0), label)
    terminal = _box(bd, (8.0, 8.0, 8.0), (8.5, 8.5, 2.0), f"{label}_terminal")
    cable = _box(bd, (6.0, 12.0, 5.0), (9.5, 25.0, 0.0), f"{label}_cable_access")
    result = _fuse_all([plate, terminal, cable])
    result.label = label
    return result


def build_fastener_envelope(*, label: str = "m4_fastener") -> Any:
    bd = _build123d()
    shaft = _cylinder_axis(bd, 2.0, 18.0, (0.0, 0.0, 0.0), "z", f"{label}_shaft")
    head = _cylinder_axis(bd, 4.0, 4.0, (0.0, 0.0, 18.0), "z", f"{label}_head")
    washer = _cylinder_axis(bd, 5.0, 1.0, (0.0, 0.0, 17.0), "z", f"{label}_washer")
    result = _fuse_all([shaft, head, washer])
    result.label = label
    return result


__all__ = [
    "HARDWARE_MODEL_REGISTER",
    "HardwareModelSpec",
    "build_608_bearing",
    "build_arduino_mega",
    "build_conductive_probe",
    "build_cnc_shield",
    "build_d2f_limit_switch",
    "build_fastener_envelope",
    "build_flexible_coupler",
    "build_mgn_carriage",
    "build_mgn_rail",
    "build_nema17",
    "build_spindle_candidate",
    "build_t8_nut",
    "build_t8_screw",
    "hardware_model_register_dicts",
]
