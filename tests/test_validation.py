"""Foundation validation tests."""

from dataclasses import replace
import unittest

from cad.parameters import INITIAL_PARAMETERS, RangeMm
from cad.validation import (
    AxisCapacity,
    PrintOrientationCandidate,
    PrintablePart,
    ValidationStatus,
    check_printable_part,
    check_project_parameters,
    check_working_envelope,
    run_foundation_checks,
    WorkingEnvelopeRequirement,
)


class FoundationValidationTests(unittest.TestCase):
    def test_initial_parameters_pass_foundation_checks(self) -> None:
        report = run_foundation_checks()
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.PASS)

    def test_reversed_z_range_fails_parameter_check(self) -> None:
        invalid = replace(
            INITIAL_PARAMETERS,
            target_z_travel_mm=RangeMm(minimum=50.0, maximum=30.0),
        )
        report = check_project_parameters(invalid)
        self.assertFalse(report.passed)
        self.assertEqual(report.status, ValidationStatus.FAIL)

    def test_axis_capacity_is_checked_against_z_upper_target(self) -> None:
        requirement = WorkingEnvelopeRequirement(
            x_travel_mm=200.0,
            y_travel_mm=150.0,
            z_travel_mm=RangeMm(minimum=30.0, maximum=50.0),
        )
        capacity = AxisCapacity(x_travel_mm=200.0, y_travel_mm=150.0, z_travel_mm=49.9)
        report = check_working_envelope(requirement, capacity)
        self.assertFalse(report.passed)
        self.assertTrue(any(issue.rule_id == "VAL-TRAVEL-Z" for issue in report.blocking_issues))

    def test_printable_part_requires_an_orientation(self) -> None:
        part = PrintablePart(name="test_part", orientations=())
        report = check_printable_part(part, (350.0, 350.0, 350.0))
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertFalse(report.passed)

    def test_printable_part_passes_with_a_fitting_candidate(self) -> None:
        part = PrintablePart(
            name="test_part",
            orientations=(
                PrintOrientationCandidate(
                    name="upright",
                    extents_mm=(100.0, 120.0, 40.0),
                    manufacturing_notes="Bed contact and critical faces are documented.",
                ),
            ),
        )
        report = check_printable_part(part, (350.0, 350.0, 350.0))
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.PASS)

    def test_printable_part_fails_when_all_candidates_are_too_large(self) -> None:
        part = PrintablePart(
            name="oversize_part",
            orientations=(
                PrintOrientationCandidate(
                    name="candidate",
                    extents_mm=(351.0, 100.0, 100.0),
                    manufacturing_notes="Candidate for negative test.",
                ),
            ),
        )
        report = check_printable_part(part, (350.0, 350.0, 350.0))
        self.assertEqual(report.status, ValidationStatus.FAIL)
        self.assertFalse(report.passed)

    def test_printable_part_requires_manufacturing_notes(self) -> None:
        part = PrintablePart(
            name="undocumented_part",
            orientations=(
                PrintOrientationCandidate(
                    name="candidate",
                    extents_mm=(100.0, 100.0, 100.0),
                    manufacturing_notes="",
                ),
            ),
        )
        report = check_printable_part(part, (350.0, 350.0, 350.0))
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertFalse(report.passed)


if __name__ == "__main__":
    unittest.main()
