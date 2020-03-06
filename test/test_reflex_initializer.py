import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.reflex_initializer import ReflexInitializer


class ReflexInitializerTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.initializer = ReflexInitializer(False, os.getcwd())

    @patch("reflex_cli.reflex_initializer.RuleDiscoverer")
    @patch("reflex_cli.reflex_initializer.ReflexInitializer.get_input")
    def test_query_possible_rules(self, input_mock, discoverer_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = "y"
        rule_mock = MagicMock()
        rule_mock.name = "test"
        rule_mock.version = "test"
        discoverer_mock = rule_mock
        discoverer_mock.discovered_rules = [rule_mock]
        test_object = ReflexInitializer(os.getcwd(), False)
        single_valid_template = test_object.query_possible_rules()
        self.assertEqual(single_valid_template, [])

        discoverer_mock.return_value = ["test"]
        no_valid_template = test_object.query_possible_rules()
        self.assertTrue(no_valid_template == [])

    @patch("reflex_cli.reflex_initializer.pkg_resources")
    def test_set_version(self, pkg_mock):
        test_object = ReflexInitializer(False, os.getcwd())
        version_mock = MagicMock()
        version_mock.version = "4.3.21"
        pkg_mock.require.return_value = [version_mock]
        test_object.set_version()
        self.assertTrue(test_object.configs["version"] == "4.3.21")

    @patch("reflex_cli.reflex_initializer.ReflexInitializer.get_input")
    def test_set_global_values(self, input_mock):
        input_mock.return_value = "example@example.com"
        empty_initializer = ReflexInitializer(False, os.getcwd())
        self.assertTrue("globals" not in empty_initializer.configs.keys())
        empty_initializer.set_global_values()
        self.assertTrue("globals" in empty_initializer.configs.keys())
        self.assertEqual(
            "example@example.com",
            empty_initializer.configs["globals"]["default_email"],
        )
