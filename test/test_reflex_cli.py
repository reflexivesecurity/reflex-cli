import unittest
from unittest.mock import patch

import click

from reflex_cli import reflex_cli


class ReflexCliTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def test_is_command_file(self):
        """Test our defaults for the environment are sane."""
        test_cli = reflex_cli.ReflexCli()
        self.assertTrue(test_cli.is_command_file("command_test.py"))
        self.assertFalse(test_cli.is_command_file("comd_test.py"))

    @patch("os.listdir")
    def test_list_commands(self, mock):
        mock.return_value = ["test"]
        test_empty_cli = reflex_cli.ReflexCli()
        self.assertEqual([], test_empty_cli.list_commands({}))

        mock.return_value = ["command_test.py"]
        self.assertEqual(["test"], test_empty_cli.list_commands({}))

    def test_get_command(self):
        test_cli_build_command = reflex_cli.ReflexCli()
        build_cli = test_cli_build_command.get_command({}, "build")

        self.assertTrue(isinstance(build_cli, click.core.Command))
