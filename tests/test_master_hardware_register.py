"""Dependency-light contracts for the hardware-first master register."""

import unittest

from cad.hardware.master_hardware import HARDWARE_MODEL_REGISTER
from cad.parameters import PHASE5_MASTER_PARAMETERS


class MasterHardwareRegisterTests(unittest.TestCase):
    def test_owner_hardware_boundary_is_explicit(self) -> None:
        records = {item.component: item for item in HARDWARE_MODEL_REGISTER}
        self.assertIn("owner-stock NEMA17 motor", records)
        self.assertIn("owner CNC Shield", records)
        self.assertEqual(records["owner-stock NEMA17 motor"].classification, "ENVELOPE-ONLY")
        self.assertEqual(records["owner CNC Shield"].classification, "PROVISIONAL")
        self.assertIn("DO NOT BUY", records["owner-stock NEMA17 motor"].repository_action)

    def test_external_sources_are_tracked_without_redistributed_cad(self) -> None:
        records = {item.component: item for item in HARDWARE_MODEL_REGISTER}
        self.assertTrue(records["MGN12 rail and MGN12H carriage"].source_url.startswith("https://"))
        self.assertTrue(records["Arduino Mega 2560 controller"].source_url.startswith("https://"))
        self.assertIn("not committed", records["ER11 spindle candidate"].license_reuse_status)
        self.assertTrue(all(item.repository_action for item in HARDWARE_MODEL_REGISTER))

    def test_master_preserves_generic_motor_and_controller_interfaces(self) -> None:
        parameters = PHASE5_MASTER_PARAMETERS
        self.assertEqual(parameters.nema17_frame_mm, 42.3)
        self.assertEqual(parameters.nema17_shaft_diameter_mm, 5.0)
        self.assertEqual(parameters.nema17_body_length_range_mm, (40.0, 48.0))
        self.assertIn("Arduino Mega + CNC Shield revision", " ".join(parameters.provisional_interfaces))
        self.assertIn("CNC Shield revision", " ".join(parameters.provisional_interfaces))


if __name__ == "__main__":
    unittest.main()
