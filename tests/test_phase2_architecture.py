"""Dependency-light tests for the Phase 2 architecture package."""

import unittest

from cad.architecture import (
    ArchitectureId,
    FORCE_LOOP_ASSESSMENTS,
    matrix_is_well_formed,
    ranked_scores,
    sensitivity_scores,
)
from cad.validation import check_phase2_skeleton_parameters


class Phase2ArchitectureTests(unittest.TestCase):
    def test_matrix_is_well_formed_and_has_a_winner(self) -> None:
        self.assertTrue(matrix_is_well_formed())
        ranking = ranked_scores()
        self.assertEqual(ranking[0][0], ArchitectureId.B)
        self.assertEqual(ranking[1][0], ArchitectureId.A)
        self.assertGreater(ranking[0][1], ranking[1][1])

    def test_sensitivity_scenarios_keep_b_as_screening_winner(self) -> None:
        for scenario in ("stiffness-led", "datum-and-probing-led", "printability-led", "service-and-access-led"):
            self.assertEqual(sensitivity_scores(scenario)[0][0], ArchitectureId.B)

    def test_force_loop_screening_keeps_b_shortest(self) -> None:
        lengths = {item.candidate_id: item.nominal_loop_length_mm for item in FORCE_LOOP_ASSESSMENTS}
        self.assertLess(lengths[ArchitectureId.B], lengths[ArchitectureId.A])
        self.assertLess(lengths[ArchitectureId.B], lengths[ArchitectureId.C])

    def test_skeleton_parameter_validation_passes(self) -> None:
        report = check_phase2_skeleton_parameters()
        self.assertTrue(report.passed)
        self.assertEqual(report.status.value, "pass")


if __name__ == "__main__":
    unittest.main()
