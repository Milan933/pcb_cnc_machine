import unittest

from tools.validate_mechanical_cad_framework import validate_framework


class MechanicalCadFrameworkTests(unittest.TestCase):
    def test_framework_contract_is_complete(self):
        self.assertEqual(validate_framework(), [])


if __name__ == "__main__":
    unittest.main()
