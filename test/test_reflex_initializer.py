import unittest
import os
from reflex_cli.reflex_initializer import ReflexInitializer
from unittest.mock import patch


class ReflexInitializerTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.initializer = ReflexInitializer(os.getcwd())

    @patch("reflex_cli.reflex_initializer.ReflexInitializer.get_input")
    def test_is_valid_template(self, mock):
        mock.return_value = "y"
        valid_template = self.initializer.is_valid_template("test.tf")
        self.assertTrue(valid_template)


#     @patch('reflex_cli.reflex_initializer.os')
#     @patch('reflex_cli.reflex_initializer.ReflexInitializer.get_input')
#     def test_query_possible_measures(self, os_mock, input_mock):
#         """Test our logic for measures is correct"""
#         input_mock.return_value = 'y'
#         os_mock.listdir.return_value = ["test.tf"]
#         single_valid_template = self.initializer.query_possible_measures()
#         self.assertTrue(single_valid_template)
#
#
#         os_mock.listdir.return_value = ["test"]
#         no_valid_template = self.initializer.query_possible_measures()
#         self.assertTrue(no_valid_template == [])
