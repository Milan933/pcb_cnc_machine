"""Compatibility exports for the hardware-first Phase 5 master structure.

The public import path is retained for existing tools and review scripts, but
the implementation now lives in :mod:`cad.parts.master_structural` and is
derived from the complete master assembly rather than the former independent
19-part envelope batch.
"""

from .master_structural import (
    MASTER_PART_DEFINITIONS,
    MASTER_PART_IDS,
    MasterPartDefinition,
    build_base_side,
    build_master_structural_parts,
)


PHASE5_COMPLETE_PART_DEFINITIONS = MASTER_PART_DEFINITIONS
PHASE5_COMPLETE_PART_IDS = MASTER_PART_IDS
Phase5PartDefinition = MasterPartDefinition


def build_phase5_complete_structural_parts():
    """Return the derived PETG solids from the master hardware layout."""

    return build_master_structural_parts()


__all__ = [
    "PHASE5_COMPLETE_PART_DEFINITIONS",
    "PHASE5_COMPLETE_PART_IDS",
    "Phase5PartDefinition",
    "build_base_side",
    "build_phase5_complete_structural_parts",
]
