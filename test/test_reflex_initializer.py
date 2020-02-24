import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.reflex_initializer import ReflexInitializer


class ReflexInitializerTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.initializer = ReflexInitializer(os.getcwd(), False)

    @patch("reflex_cli.reflex_initializer.MeasureDiscoverer")
    @patch("reflex_cli.reflex_initializer.ReflexInitializer.get_input")
    def test_query_possible_measures(self, input_mock, discoverer_mock):
        """Test our logic for measures is correct"""
        input_mock.return_value = "y"
        measure_mock = MagicMock()
        measure_mock.name = "test"
        measure_mock.version = "test"
        discoverer_mock = measure_mock
        discoverer_mock.discovered_measures = [measure_mock]
        test_object = ReflexInitializer(os.getcwd(), False)
        single_valid_template = test_object.query_possible_measures()
        self.assertEqual(single_valid_template, [])

        discoverer_mock.return_value = ["test"]
        no_valid_template = test_object.query_possible_measures()
        self.assertTrue(no_valid_template == [])

    @patch("reflex_cli.reflex_initializer.pkg_resources")
    def test_set_version(self, pkg_mock):
        test_object = ReflexInitializer(os.getcwd(), False)
        version_mock = MagicMock()
        version_mock.version = "4.3.21"
        pkg_mock.require.return_value = [version_mock]
        test_object.set_version()
        self.assertTrue(test_object.configs["version"] == "4.3.21")
