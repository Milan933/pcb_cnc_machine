"""Dependency-light contracts for the complete Phase 5 virtual machine."""

import unittest

from cad.parameters import PHASE5_COMPLETE_PARAMETERS
from cad.parts.phase5_complete_structural import (
    PHASE5_COMPLETE_PART_DEFINITIONS,
    PHASE5_COMPLETE_PART_IDS,
)
from cad.validation import (
    ValidationStatus,
    check_phase5_complete_structural_parts,
    phase5_complete_gate_report,
)


class Phase5CompleteMachineTests(unittest.TestCase):
    def test_complete_inventory_is_exactly_nineteen_stable_parts(self) -> None:
        self.assertEqual(len(PHASE5_COMPLETE_PART_IDS), 19)
        self.assertEqual(tuple(item.part_id for item in PHASE5_COMPLETE_PART_DEFINITIONS), PHASE5_COMPLETE_PART_IDS)
        self.assertEqual(tuple(item.part_number for item in PHASE5_COMPLETE_PART_DEFINITIONS), tuple(f"PCNC-P{index:03d}" for index in range(1, 20)))
        self.assertTrue(all(item.material == "PETG" for item in PHASE5_COMPLETE_PART_DEFINITIONS))
        self.assertTrue(all(item.interface_status == "PROVISIONAL_HARDWARE_DIMENSION" for item in PHASE5_COMPLETE_PART_DEFINITIONS))

    def test_coordinate_and_hardware_screening_contract(self) -> None:
        parameters = PHASE5_COMPLETE_PARAMETERS
        self.assertEqual(parameters.work_area_mm, (200.0, 150.0))
        self.assertEqual(parameters.usable_travel_mm, (220.0, 170.0, 40.0))
        self.assertEqual(parameters.travel_min_mm, (-110.0, -85.0, -25.0))
        self.assertEqual(parameters.travel_max_mm, (110.0, 85.0, 15.0))
        self.assertEqual(parameters.nema17_frame_mm, 42.3)
        self.assertEqual(parameters.nema17_shaft_diameter_mm, 5.0)
        self.assertEqual(parameters.nema17_body_length_range_mm, (40.0, 48.0))
        self.assertIn("Arduino Mega + CNC Shield revision", " ".join(parameters.provisional_interfaces))

    def test_dependency_light_part_check_fails_closed_for_missing_geometry(self) -> None:
        report = check_phase5_complete_structural_parts({})
        self.assertEqual(report.status, ValidationStatus.FAIL)
        self.assertFalse(report.passed)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE5-COMPLETE-PART-IDS" for issue in report.issues))

    def test_complete_phase_gate_is_open_but_not_release(self) -> None:
        report = phase5_complete_gate_report()
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertTrue(report.passed)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE5-COMPLETE-AUTHORIZATION" for issue in report.issues))
        self.assertTrue(any(issue.rule_id == "VAL-PHASE5-COMPLETE-MATURITY" for issue in report.issues))


if __name__ == "__main__":
    unittest.main()
