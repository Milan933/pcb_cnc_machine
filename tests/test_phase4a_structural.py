"""Dependency-light tests for the proposed Phase 4A optimization study."""

import unittest

from cad.phase4a_calculations import phase4a_structural_estimate
from cad.parts.phase4a_structural import (
    PHASE4A_VARIANTS,
    PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT,
    SELECTED_PHASE4A_VARIANT,
    VARIANT_ORDER,
    PRIMARY_LOOP_BY_VARIANT,
)
from cad.validation import ValidationStatus, phase4a_gate_report


class Phase4AStructuralOptimizationTests(unittest.TestCase):
    def test_three_optimization_levels_and_selected_compromise_are_controlled(self) -> None:
        self.assertEqual(VARIANT_ORDER, ("O1", "O2", "O3"))
        self.assertEqual(tuple(item.variant_id for item in PHASE4A_VARIANTS), VARIANT_ORDER)
        self.assertEqual(SELECTED_PHASE4A_VARIANT, "O2")

    def test_all_variants_pass_preferred_preliminary_deflection_screen(self) -> None:
        for variant_id in VARIANT_ORDER:
            estimate = phase4a_structural_estimate(variant_id)
            self.assertTrue(estimate.target_passes, variant_id)
            self.assertTrue(estimate.preferred_target_passes, variant_id)
            self.assertTrue(estimate.acceptance_passes, variant_id)
            self.assertLessEqual(estimate.total_tool_point_deflection_mm, 0.015, variant_id)

    def test_primary_loop_parts_and_joint_register_shrink_with_integration(self) -> None:
        self.assertEqual(
            {variant: len(PRIMARY_LOOP_BY_VARIANT[variant]) for variant in VARIANT_ORDER},
            {"O1": 17, "O2": 9, "O3": 7},
        )
        self.assertEqual(
            dict(PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT),
            {"O1": 17, "O2": 7, "O3": 5},
        )

    def test_phase4a_gate_records_phase5_candidate_boundary(self) -> None:
        report = phase4a_gate_report()
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE4A-PHASE5-RELEASE-GATE" for issue in report.issues))
        self.assertTrue(all(issue.severity.value == "warning" for issue in report.issues if issue.rule_id == "VAL-PHASE4A-GATE-EVIDENCE"))


if __name__ == "__main__":
    unittest.main()
