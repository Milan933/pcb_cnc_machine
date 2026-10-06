"""Tests for the PETG insert and selective through-bolt strategy."""

from dataclasses import replace
import unittest

from cad.fastening import check_fastener_interface, check_fastening_strategy
from cad.parameters import (
    FastenerInterfaceParameter,
    PHASE3A_FASTENER_INTERFACE_SCREENS,
    PHASE3A_FASTENER_STRATEGY,
)
from cad.validation import ValidationStatus


class FasteningStrategyTests(unittest.TestCase):
    def test_standard_hierarchy_is_exactly_m3_m4_m5(self) -> None:
        report = check_fastening_strategy()
        self.assertEqual(PHASE3A_FASTENER_STRATEGY.allowed_insert_sizes, ("M3", "M4", "M5"))
        self.assertEqual(report.status, ValidationStatus.NOT_READY)
        self.assertTrue(report.passed)
        self.assertFalse(report.blocking_issues)
        self.assertTrue(
            any(issue.rule_id == "VAL-FASTEN-MEASURE-BEFORE-MANUFACTURE" for issue in report.issues)
        )

    def test_review_interface_requires_geometric_load_transfer(self) -> None:
        interface = replace(
            PHASE3A_FASTENER_INTERFACE_SCREENS[0],
            requires_selected_insert=False,
            load_transfer_features=(),
        )
        report = check_fastener_interface(interface)
        self.assertEqual(report.status, ValidationStatus.FAIL)
        self.assertTrue(any(issue.rule_id == "VAL-FASTEN-GEOMETRIC-TRANSFER" for issue in report.blocking_issues))

    def test_review_interface_can_pass_with_mechanical_seating(self) -> None:
        interface = replace(PHASE3A_FASTENER_INTERFACE_SCREENS[0], requires_selected_insert=False)
        report = check_fastener_interface(interface)
        self.assertTrue(report.passed)
        self.assertEqual(report.status, ValidationStatus.PASS)

    def test_boss_edge_and_tool_access_screens_fail_closed(self) -> None:
        interface = replace(
            PHASE3A_FASTENER_INTERFACE_SCREENS[0],
            requires_selected_insert=False,
            boss_wall_mm=2.0,
            edge_distance_mm=3.0,
            installation_tool_access_mm=(1.0, 1.0, 1.0),
        )
        report = check_fastener_interface(interface)
        self.assertEqual(report.status, ValidationStatus.FAIL)
        rule_ids = {issue.rule_id for issue in report.blocking_issues}
        self.assertIn("VAL-FASTEN-BOSS-WALL", rule_ids)
        self.assertIn("VAL-FASTEN-EDGE-DISTANCE", rule_ids)
        self.assertIn("VAL-FASTEN-TOOL-ACCESS", rule_ids)

    def test_through_bolt_requires_justification_and_geometry(self) -> None:
        interface = FastenerInterfaceParameter(
            interface_id="negative_through_bolt",
            function="Negative test",
            fastening_mode="through_bolt",
            insert_size=None,
            boss_wall_mm=6.0,
            edge_distance_mm=8.0,
            installation_tool_access_mm=(16.0, 16.0, 16.0),
            load_transfer_features=("planar seat",),
            serviceable=True,
        )
        report = check_fastener_interface(interface)
        self.assertEqual(report.status, ValidationStatus.FAIL)
        self.assertTrue(any(issue.rule_id == "VAL-FASTEN-THROUGH-BOLT" for issue in report.blocking_issues))

    def test_m5_requires_a_size_justification(self) -> None:
        interface = replace(
            PHASE3A_FASTENER_INTERFACE_SCREENS[-1],
            requires_selected_insert=False,
            size_justification=None,
        )
        report = check_fastener_interface(interface)
        self.assertEqual(report.status, ValidationStatus.FAIL)
        self.assertTrue(any(issue.rule_id == "VAL-FASTEN-M5-JUSTIFICATION" for issue in report.blocking_issues))


if __name__ == "__main__":
    unittest.main()
