import unittest
import os
from reflex_cli import config_parser


class ConfigParserTestCase(unittest.TestCase):
    def setUp(self):
        self.test_config_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/reflex.yaml")
        )

    def test_generate_config_returns_dictionary(self):
        fresh_config = config_parser.ConfigParser(self.test_config_file)
        self.assertTrue(isinstance(fresh_config.generate_config(), dict))
