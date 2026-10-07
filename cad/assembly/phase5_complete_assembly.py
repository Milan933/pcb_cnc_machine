"""Compatibility exports for the Phase 5 hardware-first master assembly."""

from .master_machine import (
    MasterAssemblyComponent as CompleteAssemblyComponent,
    MasterMachineAssembly as CompleteMachineAssembly,
    build_master_machine,
    build_master_travel_state,
)


def build_phase5_complete_assembly(*args, **kwargs):
    """Build the complete master machine at a deterministic travel state."""

    return build_master_machine(*args, **kwargs)


def build_phase5_travel_state(*args, **kwargs):
    """Build one of the master machine's travel states."""

    return build_master_travel_state(*args, **kwargs)


__all__ = [
    "CompleteAssemblyComponent",
    "CompleteMachineAssembly",
    "build_phase5_complete_assembly",
    "build_phase5_travel_state",
]
