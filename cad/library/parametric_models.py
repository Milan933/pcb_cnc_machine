"""Stable project-generated model entry points for the hardware library.

The first library migration deliberately keeps the proven geometry implementation
in ``cad.hardware.master_hardware`` for compatibility with earlier Phase 5
imports.  These named wrappers are the persistent public API used by the master
assembly and by the library manifest.  They prevent future assembly code from
silently selecting a different generic builder or supplier variant.
"""

from __future__ import annotations

from typing import Any

from cad.hardware.master_hardware import (
    build_608_bearing,
    build_arduino_mega,
    build_cnc_shield,
    build_conductive_probe,
    build_d2f_limit_switch,
    build_fastener_envelope,
    build_flexible_coupler,
    build_mgn_carriage,
    build_mgn_rail,
    build_nema17,
    build_spindle_candidate,
    build_t8_nut,
    build_t8_screw,
)


def build_mgn12_rail(axis: str, length_mm: float, *, label: str = "mgn12_rail") -> Any:
    return build_mgn_rail(axis, length_mm, size=12, label=label)


def build_mgn12_carriage(axis: str, *, label: str = "mgn12h_carriage") -> Any:
    return build_mgn_carriage(axis, size=12, label=label)


def build_mgn9_rail(axis: str, length_mm: float, *, label: str = "mgn9_rail") -> Any:
    return build_mgn_rail(axis, length_mm, size=9, label=label)


def build_mgn9_carriage(axis: str, *, label: str = "mgn9h_carriage") -> Any:
    return build_mgn_carriage(axis, size=9, label=label)


def build_t8x4_screw(axis: str, length_mm: float, *, label: str = "t8x4_screw") -> Any:
    return build_t8_screw(axis, length_mm, 4.0, label=label)


def build_t8x2_screw(axis: str, length_mm: float, *, label: str = "t8x2_screw") -> Any:
    return build_t8_screw(axis, length_mm, 2.0, label=label)


def build_t8_antibacklash_nut(*, label: str = "t8_antibacklash_nut") -> Any:
    return build_t8_nut(label=label)


def build_608_reference_bearing(axis: str, *, label: str = "bearing_608_reference") -> Any:
    return build_608_bearing(axis, label=label)


def build_5x8_flexible_coupler(axis: str, *, label: str = "coupler_5x8_reference") -> Any:
    return build_flexible_coupler(axis, label=label)


def build_nema17_reference(axis: str, *, label: str = "nema17_reference") -> Any:
    return build_nema17(axis, label=label)


def build_arduino_mega_reference(*, label: str = "arduino_mega_reference") -> Any:
    return build_arduino_mega(label=label)


def build_cnc_shield_provisional(*, label: str = "cnc_shield_provisional") -> Any:
    return build_cnc_shield(label=label)


def build_spindle_5045_er11_reference(*, label: str = "spindle_5045_er11_reference") -> Any:
    return build_spindle_candidate(label=label)


def build_omron_d2f_reference(*, label: str = "omron_d2f_reference") -> Any:
    return build_d2f_limit_switch(label=label)


def build_conductive_probe_reference(*, label: str = "conductive_probe_reference") -> Any:
    return build_conductive_probe(label=label)


def build_m4_fastener_reference(*, label: str = "m4_fastener_reference") -> Any:
    return build_fastener_envelope(label=label)


__all__ = [name for name in globals() if name.startswith("build_")]
