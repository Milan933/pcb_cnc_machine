"""Dependency-light contracts for the hardware-first master register."""

import unittest

from cad.library.registry import (
    hardware_library_entries,
    hardware_library_manifest_dict,
    hardware_model_id_for_instance,
    validate_hardware_library_manifest,
)
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

    def test_persistent_library_manifest_is_valid_and_stable(self) -> None:
        manifest = hardware_library_manifest_dict()
        self.assertEqual(validate_hardware_library_manifest(manifest), ())
        entries = hardware_library_entries()
        self.assertEqual(len(entries), 14)
        ids = [entry["component_id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        summary = manifest["provenance_summary"]
        self.assertEqual(summary["external_cad_models_discovered"], 6)
        self.assertEqual(summary["external_cad_models_downloaded"], 0)
        self.assertEqual(summary["external_cad_models_legally_committed"], 0)
        self.assertEqual(summary["project_generated_reference_models"], 14)

    def test_master_instance_patterns_resolve_to_library_ids(self) -> None:
        expected = {
            "x_rail_lower": "HW-LM-MGN12H-REF",
            "z_carriage_right_2": "HW-LM-MGN9H-REF",
            "x_lead_screw": "HW-LS-T8X4-ENV",
            "z_lead_screw": "HW-LS-T8X2-ENV",
            "y_fixed_bearing_cartridge": "HW-BRG-608-REF",
            "x_motor_nema17": "HW-MOTOR-NEMA17-REF",
            "arduino_mega_owner_hardware": "HW-CTRL-ARDUINO-MEGA-REF",
            "cnc_shield_owner_hardware": "HW-CTRL-CNC-SHIELD-PROV",
            "spindle_5045_ac_er11": "HW-SPINDLE-5045-ER11-001",
            "x_home_limit": "HW-SW-D2F-REF",
            "conductive_probe": "HW-PROBE-CONDUCTIVE-REF",
            "representative_m4_fastener": "HW-FST-M4-REF",
        }
        for instance_name, component_id in expected.items():
            self.assertEqual(hardware_model_id_for_instance(instance_name), component_id)
        self.assertIsNone(hardware_model_id_for_instance("pcb_envelope"))


if __name__ == "__main__":
    unittest.main()
