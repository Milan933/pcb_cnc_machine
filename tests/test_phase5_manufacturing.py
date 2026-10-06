"""Dependency-light tests for the first Phase 5 manufacturing-CAD batch."""

import unittest

from cad.parts.phase5_structural import (
    PHASE5_BASE_PAIR_PARAMETERS,
    PHASE5_BASE_PART_IDS,
)
from cad.validation import ValidationStatus, phase5_gate_report


class Phase5ManufacturingCadTests(unittest.TestCase):
    def test_base_pair_contract_is_printable_and_provisional(self) -> None:
        parameters = PHASE5_BASE_PAIR_PARAMETERS
        self.assertEqual(PHASE5_BASE_PART_IDS, ("base_left_integrated", "base_right_integrated"))
        self.assertEqual(parameters.part_width_mm, 150.0)
        self.assertEqual(parameters.part_length_mm, 300.0)
        self.assertEqual(parameters.overall_height_mm, 43.75)
        self.assertLessEqual(max(parameters.part_width_mm, parameters.part_length_mm), 320.0)
        self.assertEqual(parameters.maturity, "PROTOTYPE-STL")
        self.assertEqual(parameters.interface_status, "PROVISIONAL_HARDWARE_DIMENSION")
        self.assertEqual(len(parameters.rail_hole_y_positions_mm), parameters.rail_hole_count)

    def test_phase5_gate_is_open_for_first_batch_but_not_release(self) -> None:
        report = phase5_gate_report()
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE5-AUTHORIZATION" for issue in report.issues))
        self.assertTrue(any(issue.rule_id == "VAL-PHASE5-RELEASE-BOUNDARY" for issue in report.issues))
        self.assertTrue(report.passed)


if __name__ == "__main__":
    unittest.main()
