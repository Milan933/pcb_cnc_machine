"""Dependency-light tests for the focused Phase 2A A-versus-B study."""

from dataclasses import replace
import unittest

from cad.architecture import ArchitectureId
from cad.parameters import PHASE2A_PARAMETERS
from cad.phase2a import (
    PHASE2A_SCORES,
    dynamic_estimate,
    mass_breakdown,
    phase2a_is_well_formed,
    phase2a_ranking,
    phase2a_sensitivity,
    racking_estimate,
    structural_estimate,
)
from cad.validation import check_phase2a_parameters


class Phase2AStructuralStudyTests(unittest.TestCase):
    def test_inputs_and_revised_matrix_are_well_formed(self) -> None:
        self.assertTrue(check_phase2a_parameters().passed)
        self.assertTrue(phase2a_is_well_formed())
        self.assertEqual(PHASE2A_SCORES[ArchitectureId.A], (5, 5, 4, 3, 5, 4, 4, 3, 2, 2, 3))
        self.assertEqual(PHASE2A_SCORES[ArchitectureId.B], (4, 4, 3, 5, 2, 3, 2, 4, 5, 5, 4))
        self.assertEqual(phase2a_ranking()[0][0], ArchitectureId.A)
        self.assertAlmostEqual(phase2a_ranking()[0][1], 78.0)
        self.assertAlmostEqual(phase2a_ranking()[1][1], 75.2)

    def test_analytical_deflection_is_additive_and_target_results_are_explicit(self) -> None:
        a = structural_estimate(ArchitectureId.A)
        b = structural_estimate(ArchitectureId.B)
        self.assertAlmostEqual(a.direct_stack_mm, 0.00857429984095, places=12)
        self.assertAlmostEqual(a.total_tool_point_displacement_mm, 0.01107429984095, places=12)
        self.assertAlmostEqual(b.direct_stack_mm, 0.0219151883075, places=12)
        self.assertAlmostEqual(b.total_tool_point_displacement_mm, 0.0269151883075, places=12)
        self.assertLess(a.total_tool_point_displacement_mm, 0.020)
        self.assertGreater(b.total_tool_point_displacement_mm, 0.020)
        self.assertLessEqual(b.total_tool_point_displacement_mm, 0.030)
        self.assertAlmostEqual(sum(item.displacement_mm for item in a.contributions), a.total_tool_point_displacement_mm)
        self.assertAlmostEqual(sum(percentage for _, percentage in a.contribution_percentages), 100.0)
        self.assertAlmostEqual(sum(percentage for _, percentage in b.contribution_percentages), 100.0)

    def test_mass_dynamic_and_racking_screens_are_quantified(self) -> None:
        self.assertAlmostEqual(mass_breakdown(ArchitectureId.A).total_kg, 1.24)
        self.assertAlmostEqual(mass_breakdown(ArchitectureId.B).total_kg, 3.95)
        self.assertAlmostEqual(dynamic_estimate(ArchitectureId.A).y_screw_design_force_n, 1.498)
        self.assertAlmostEqual(dynamic_estimate(ArchitectureId.B).y_screw_design_force_n, 2.54)
        self.assertGreater(
            dynamic_estimate(ArchitectureId.A).relative_resonance_index,
            dynamic_estimate(ArchitectureId.B).relative_resonance_index,
        )
        a_racking = racking_estimate(ArchitectureId.A)
        b_racking = racking_estimate(ArchitectureId.B)
        self.assertTrue(a_racking.centered_screw_credible)
        self.assertTrue(b_racking.centered_screw_credible)
        self.assertAlmostEqual(a_racking.differential_guide_force_n, 2.2727272727, places=9)
        self.assertLess(a_racking.estimated_edge_displacement_mm, b_racking.estimated_edge_displacement_mm)

    def test_sensitivity_exposes_the_close_process_trade(self) -> None:
        self.assertEqual(phase2a_sensitivity("structural-evidence-heavy")[0][0], ArchitectureId.A)
        self.assertEqual(phase2a_sensitivity("calibration-and-usability-heavy")[0][0], ArchitectureId.B)
        self.assertEqual(phase2a_sensitivity("manufacturing-heavy")[0][0], ArchitectureId.A)
        self.assertEqual(phase2a_sensitivity("moving-mass-heavy")[0][0], ArchitectureId.A)

    def test_phase2a_rejects_architecture_c(self) -> None:
        with self.assertRaises(ValueError):
            structural_estimate(ArchitectureId.C)
        with self.assertRaises(ValueError):
            mass_breakdown(ArchitectureId.C)

    def test_phase2a_input_validation_fails_closed(self) -> None:
        invalid = replace(PHASE2A_PARAMETERS, b_section_wall_mm=40.0)
        report = check_phase2a_parameters(invalid)
        self.assertFalse(report.passed)
        self.assertTrue(any(issue.rule_id == "VAL-PHASE2A-SECTION" for issue in report.blocking_issues))


if __name__ == "__main__":
    unittest.main()
