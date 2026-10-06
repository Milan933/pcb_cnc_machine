"""Tests for the quantitative Phase 1 requirements baseline."""

import unittest

from cad.parameters import (
    PHASE1_REQUIREMENTS,
    non_compensatable_z_budget_mm,
)
from cad.validation import (
    ValidationStatus,
    check_phase1_requirements,
    v_bit_isolation_width_mm,
    v_bit_width_sensitivity,
)


class Phase1RequirementTests(unittest.TestCase):
    def test_phase1_baseline_is_internally_consistent(self) -> None:
        report = check_phase1_requirements()
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.PASS)

    def test_v_bit_width_equation(self) -> None:
        self.assertAlmostEqual(
            v_bit_isolation_width_mm(0.10, 60.0),
            0.115470,
            places=5,
        )
        self.assertAlmostEqual(
            v_bit_isolation_width_mm(0.10, 30.0),
            0.053590,
            places=5,
        )

    def test_v_bit_sensitivity_is_angle_dependent(self) -> None:
        self.assertAlmostEqual(v_bit_width_sensitivity(60.0), 1.154700, places=5)
        self.assertLess(v_bit_width_sensitivity(30.0), v_bit_width_sensitivity(60.0))

    def test_non_compensatable_z_allocations_fit_budget(self) -> None:
        self.assertAlmostEqual(
            non_compensatable_z_budget_mm(),
            PHASE1_REQUIREMENTS.z_machine_error_budget_mm,
            places=9,
        )

    def test_recommended_working_area_is_one_of_the_options(self) -> None:
        option_ids = {
            option.option_id for option in PHASE1_REQUIREMENTS.working_area_options
        }
        self.assertIn(
            PHASE1_REQUIREMENTS.recommended_working_area_option_id,
            option_ids,
        )


if __name__ == "__main__":
    unittest.main()
