"""Tests for the Phase 3A compact packaging study."""

import unittest

from cad.packaging_phase3a import (
    carriage_group_span_mm,
    minimum_rail_length_mm,
    phase3a_packaging_study,
)
from cad.parameters import PHASE3A_PACKAGING_VARIANTS, PHASE3_MOTION_PARAMETERS
from cad.validation import ValidationStatus, check_phase3a_all_variants


class Phase3APackagingTests(unittest.TestCase):
    def test_all_declared_variants_pass_dependency_light_screen(self) -> None:
        report = check_phase3a_all_variants()
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.PASS)

    def test_two_carriage_group_is_included_in_rail_stack(self) -> None:
        group = carriage_group_span_mm("MGN12H", (-30.0, 30.0))
        self.assertAlmostEqual(group, 107.6)
        self.assertAlmostEqual(minimum_rail_length_mm(220.0, group, 6.0), 339.6)

    def test_phase3_reference_lengths_do_not_prove_full_swept_travel(self) -> None:
        x_group = carriage_group_span_mm("MGN12H", (-23.8, 23.8))
        y_group = carriage_group_span_mm("MGN12H", (-50.0, 50.0))
        z_group = carriage_group_span_mm("MGN9H", (-20.0, 20.0))
        self.assertGreater(minimum_rail_length_mm(220.0, x_group, 0.0), 300.0)
        self.assertGreater(minimum_rail_length_mm(170.0, y_group, 0.0), 280.0)
        self.assertGreater(minimum_rail_length_mm(40.0, z_group, 0.0), 100.0)

    def test_p2_keeps_full_phase3_xy_travel_and_balanced_bed(self) -> None:
        variant = next(item for item in PHASE3A_PACKAGING_VARIANTS if item.variant_id == "P2")
        study = phase3a_packaging_study(variant)
        self.assertEqual(variant.tool_travel_mm, PHASE3_MOTION_PARAMETERS.screened_travel_mm)
        self.assertEqual(study.bed.pcb_edge_margin_mm, (15.0, 15.0))
        self.assertAlmostEqual(study.bed.transverse_bed_overhang_mm, 5.0)
        self.assertGreater(study.bed.longitudinal_bed_overhang_mm, 0.0)
        self.assertAlmostEqual(study.bed.swept_bed_end_clearance_mm, 3.0)
        self.assertAlmostEqual(study.bed.bed_to_y_motor_clearance_mm, 4.85)

    def test_p3_is_conditional_on_tight_workholding_and_end_margins(self) -> None:
        variant = next(item for item in PHASE3A_PACKAGING_VARIANTS if item.variant_id == "P3")
        study = phase3a_packaging_study(variant)
        self.assertEqual(study.bed.low_profile_workholding_margin_mm, 10.0)
        self.assertEqual(study.bed.vacuum_perimeter_status[:7], "vacuum ")
        self.assertLess(study.axes[0].actual_end_margin_mm, 10.0)

    def test_compact_z_stack_is_calculated_from_overlapping_envelopes(self) -> None:
        variant = next(item for item in PHASE3A_PACKAGING_VARIANTS if item.variant_id == "P2")
        stack = phase3a_packaging_study(variant).z_stack
        self.assertGreater(stack.z_motor_top_mm, stack.tool_and_spindle_top_mm)
        self.assertAlmostEqual(stack.package_height_mm, 276.0)
        self.assertLess(stack.package_height_mm, 300.65)


if __name__ == "__main__":
    unittest.main()
