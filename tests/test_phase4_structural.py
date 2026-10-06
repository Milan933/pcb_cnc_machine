"""Dependency-light tests for the Phase 4 preliminary structural concept."""

from dataclasses import replace
import unittest

from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS, ParameterStatus
from cad.phase4_calculations import phase4_structural_estimate
from cad.validation import (
    ValidationStatus,
    check_phase4_structural_parameters,
)


class Phase4StructuralConceptTests(unittest.TestCase):
    def test_part_decomposition_stays_within_the_owner_print_boundary(self) -> None:
        parameters = PHASE4_STRUCTURAL_PARAMETERS
        self.assertEqual(parameters.reference_variant_id, "P2")
        self.assertEqual(len(parameters.print_parts), 29)
        self.assertTrue(
            all(
                max(part.print_orientation_extents_mm[:2]) <= parameters.conservative_structural_xy_mm
                for part in parameters.print_parts
                if part.mandatory
            )
        )
        self.assertTrue(
            any(max(part.print_orientation_extents_mm[:2]) == parameters.preferred_structural_xy_mm for part in parameters.print_parts)
        )
        self.assertTrue(all(part.status == ParameterStatus.PRELIMINARY for part in parameters.print_parts))

    def test_joint_study_selects_only_j1_provisionally(self) -> None:
        concepts = PHASE4_STRUCTURAL_PARAMETERS.joint_concepts
        self.assertEqual({concept.concept_id for concept in concepts}, {"J1", "J2", "J3"})
        self.assertEqual([concept.concept_id for concept in concepts if concept.selected], ["J1"])

    def test_structural_screen_passes_both_target_and_acceptance(self) -> None:
        estimate = phase4_structural_estimate()
        self.assertTrue(estimate.target_passes)
        self.assertTrue(estimate.acceptance_passes)
        self.assertLessEqual(estimate.total_tool_point_deflection_mm, estimate.target_mm)
        self.assertAlmostEqual(
            sum(item.displacement_mm for item in estimate.contributions),
            estimate.total_tool_point_deflection_mm,
        )
        self.assertIn(estimate.dominant_contribution, {item.name for item in estimate.contributions})

    def test_parameter_report_is_clear_but_gate_evidence_remains_explicit(self) -> None:
        report = check_phase4_structural_parameters()
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE4-CALCULATION-EVIDENCE" for issue in report.issues))

    def test_mandatory_part_over_320_mm_fails_closed(self) -> None:
        first = PHASE4_STRUCTURAL_PARAMETERS.print_parts[0]
        oversized = replace(first, print_orientation_extents_mm=(321.0, 100.0, 50.0))
        invalid = replace(
            PHASE4_STRUCTURAL_PARAMETERS,
            print_parts=(oversized,) + PHASE4_STRUCTURAL_PARAMETERS.print_parts[1:],
        )
        report = check_phase4_structural_parameters(invalid)
        self.assertFalse(report.passed)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE4-PRINT-BOUND" for issue in report.blocking_issues))


if __name__ == "__main__":
    unittest.main()
