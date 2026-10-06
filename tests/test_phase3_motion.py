"""Tests for the Phase 3 motion-system screening package."""

import unittest

from cad.motion_phase3 import (
    command_increment_mm,
    phase3_motion_screen,
    screw_critical_speed_rpm,
    screw_input_torque_nm,
    steps_per_mm,
)
from cad.parameters import PHASE3_MOTION_PARAMETERS
from cad.validation import (
    ValidationStatus,
    check_phase3_motion_parameters,
    phase3_gate_report,
)


class Phase3MotionTests(unittest.TestCase):
    def test_phase3_parameter_integrity_passes(self) -> None:
        report = check_phase3_motion_parameters()
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.PASS)

    def test_gate_remains_not_ready_without_hardware_evidence(self) -> None:
        report = phase3_gate_report()
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertFalse(report.passed)
        self.assertGreaterEqual(len(report.blocking_issues), 5)

    def test_t8_resolution_is_command_resolution_only(self) -> None:
        self.assertAlmostEqual(steps_per_mm(4.0, 1), 50.0)
        self.assertAlmostEqual(command_increment_mm(4.0, 8), 0.0025)
        self.assertAlmostEqual(command_increment_mm(2.0, 16), 0.000625)

    def test_screw_torque_screen(self) -> None:
        self.assertAlmostEqual(screw_input_torque_nm(50.0, 4.0, 0.35), 0.090946, places=5)
        self.assertAlmostEqual(screw_input_torque_nm(50.0, 2.0, 0.35), 0.045473, places=5)

    def test_screw_whip_screen_matches_documented_lengths(self) -> None:
        x_rpm = screw_critical_speed_rpm(300.0, 6.2, 200000.0, 7.85e-6)
        y_rpm = screw_critical_speed_rpm(280.0, 6.2, 200000.0, 7.85e-6)
        z_rpm = screw_critical_speed_rpm(120.0, 6.2, 200000.0, 7.85e-6)
        self.assertAlmostEqual(x_rpm, 259.084, places=2)
        self.assertAlmostEqual(y_rpm, 297.418, places=2)
        self.assertAlmostEqual(z_rpm, 1619.275, places=2)
        self.assertGreater(z_rpm, x_rpm)

    def test_selected_axes_and_moment_reactions(self) -> None:
        screen = phase3_motion_screen()
        by_axis = {item.axis: item for item in screen.axes}
        self.assertEqual(by_axis["X"].rail_class, "MGN12H")
        self.assertEqual(by_axis["Y"].rail_center_spacing_mm, 220.0)
        self.assertEqual(by_axis["Z"].screw.lead_mm, 2.0)
        self.assertAlmostEqual(by_axis["Y"].guide_moment_reaction_n, 250.0 / 220.0)
        self.assertAlmostEqual(by_axis["Z"].racking_moment_reaction_n, 500.0 / 60.0)
        self.assertAlmostEqual(screen.pcb_edge_margin_mm[0], 20.0)
        self.assertAlmostEqual(screen.pcb_edge_margin_mm[1], 20.0)

    def test_feed_screen_is_below_the_whip_margin(self) -> None:
        screen = phase3_motion_screen()
        for axis in screen.axes:
            self.assertLessEqual(
                axis.screw.commissioning_feed_mm_min,
                axis.screw.screened_max_feed_mm_min,
            )

    def test_phase3_central_axes_cover_screened_travel(self) -> None:
        travel = PHASE3_MOTION_PARAMETERS.screened_travel_mm
        axes = {axis.axis: axis for axis in PHASE3_MOTION_PARAMETERS.axes}
        self.assertEqual(tuple(axes[name].travel_mm for name in ("X", "Y", "Z")), travel)
        self.assertEqual(PHASE3_MOTION_PARAMETERS.recommended_microsteps, 8)


if __name__ == "__main__":
    unittest.main()
