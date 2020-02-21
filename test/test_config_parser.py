import os
import unittest

from reflex_cli import config_parser


class ConfigParserTestCase(unittest.TestCase):
    def setUp(self):
        self.test_config_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/reflex.yaml")
        )
        self.test_config = config_parser.ConfigParser(self.test_config_file)

    def test_generate_config_returns_dictionary(self):
        self.assertTrue(isinstance(self.test_config.generate_config(), dict))

    def test_validate_config(self):
        empty_config = {}
        self.assertFalse(self.test_config.validate_config(empty_config))

        config_key_no_value = {"version": None}
        self.assertFalse(self.test_config.validate_config(config_key_no_value))

        test_config_dict = self.test_config.generate_config()
        self.assertTrue(self.test_config.validate_config(test_config_dict))
