import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.user_input import UserInput


class UserInputTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.user_input = UserInput(True)

    @patch("reflex_cli.user_input.UserInput.get_input")
    def test_collect_default_email(self, input_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = "example@example.com"
        select_all_input = UserInput(False)
        self.assertEqual(
            "placeholder@example.com", select_all_input.collect_default_email()
        )

        no_select_all_input = UserInput(True)
        self.assertEqual(
            "example@example.com", no_select_all_input.collect_default_email()
        )

    @patch("reflex_cli.user_input.UserInput.get_input")
    def test_verify_rule(self, input_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = "y"
        test = MagicMock()
        test.name = "example"
        test.version = "example"
        self.assertTrue(self.user_input.verify_rule(test))

    @patch("reflex_cli.user_input.UserInput.verify_rule")
    def test_get_rule_input(self, input_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = True
        test = MagicMock()
        test.name = "example"
        test.version = None

        self.assertEqual([], self.user_input.get_rule_input([test]))

        test2 = MagicMock()
        test2.name = "first"
        test2.version = "example"
        test2.configurables = None

        self.assertEqual(
            [{"first": {"version": "example"}}],
            self.user_input.get_rule_input([test2]),
        )

        test3 = MagicMock()
        test3.name = "first"
        test3.version = "example"
        test3.configurables = ["mode"]

        self.assertEqual(
            [{"first": {"version": "example", "configuration": {"mode": ""}}}],
            self.user_input.get_rule_input([test3]),
        )

        test4 = MagicMock()
        test4.name = "first"
        test4.version = "example"
        test4.configurables = [{"mode": "detect"}]

        self.assertEqual(
            [
                {
                    "first": {
                        "version": "example",
                        "configuration": {"mode": "detect"},
                    }
                }
            ],
            self.user_input.get_rule_input([test4]),
        )

    @patch("reflex_cli.user_input.UserInput.get_input")
    def test_get_backend_key_values(self, input_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = "N"
        key_values = self.user_input.collect_backend_key_values()
        self.assertEqual(key_values, [{"N": "N"}])

    @patch("reflex_cli.user_input.UserInput.get_input")
    @patch("reflex_cli.user_input.UserInput.collect_backend_key_values")
    def test_get_backend_config(self, key_values, input_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = "y"
        key_values.return_value = [{"bucket": "s3-bucket"}]
        backend_config = self.user_input.get_backend_configuration()
        self.assertEqual(backend_config, {"y": [{"bucket": "s3-bucket"}]})

    @patch("reflex_cli.user_input.UserInput.get_input")
    @patch("os.environ.get")
    def test_get_region(self, environment_variables, input_mock):
        """Test our logic for rules is correct"""
        input_mock.return_value = "us-east-1"
        environment_variables.return_value = None
        all_input = UserInput(False)
        self.assertIsNone(all_input.get_region())
        self.assertEqual("us-east-1", self.user_input.get_region())

    @patch("reflex_cli.user_input.UserInput.get_input")
    @patch("reflex_cli.user_input.UserInput.ask_to_overwrite")
    def test_verify_upgrade_interested(self, overwrite_mock, input_mock):
        """Test our logic for rules is correct"""
        overwrite_mock.return_value = True
        all_input = UserInput(False)
        self.assertTrue(all_input.verify_upgrade_interest())
