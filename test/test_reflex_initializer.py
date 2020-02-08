import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.reflex_initializer import ReflexInitializer


class ReflexInitializerTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.initializer = ReflexInitializer(os.getcwd())

    @patch("reflex_cli.reflex_initializer.ReflexInitializer.get_input")
    def test_is_valid_template(self, mock):
        mock.return_value = "y"
        valid_template = self.initializer.is_valid_template("test.tf")
        self.assertTrue(valid_template)

    @patch("reflex_cli.reflex_initializer.os.listdir")
    @patch("reflex_cli.reflex_initializer.ReflexInitializer.get_input")
    def test_query_possible_measures(self, input_mock, os_mock):
        """Test our logic for measures is correct"""
        input_mock.return_value = "y"
        os_mock.return_value = ["test.tf"]
        test_object = ReflexInitializer(os.getcwd())
        single_valid_template = test_object.query_possible_measures()
        self.assertTrue(single_valid_template)

        os_mock.return_value = ["test"]
        no_valid_template = test_object.query_possible_measures()
        self.assertTrue(no_valid_template == [])

    @patch("reflex_cli.reflex_initializer.pkg_resources")
    def test_set_version(self, pkg_mock):
        test_object = ReflexInitializer(os.getcwd())
        version_mock = MagicMock()
        version_mock.version = "4.3.21"
        pkg_mock.require.return_value = [version_mock]
        test_object.set_version()
        self.assertTrue(test_object.configs["version"] == "4.3.21")
