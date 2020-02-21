import os
import unittest

from reflex_cli import cli_environment


class CliEnvironmentTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def test_environment_defaults(self):
        """Test our defaults for the environment are sane."""
        fresh_environment = cli_environment.CliEnvironment()
        self.assertFalse(fresh_environment.verbose)
        self.assertEqual(fresh_environment.home, os.getcwd())
