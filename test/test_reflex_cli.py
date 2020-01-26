import unittest
import os
from reflex_cli import reflex_cli


class ReflexCliTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def test_is_command_file(self):
        """Test our defaults for the environment are sane."""
        test_cli = reflex_cli.ReflexCli()
        self.assertTrue(test_cli.is_command_file('command_test.py'))
        self.assertFalse(test_cli.is_command_file('comd_test.py'))
