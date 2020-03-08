import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.rule import Rule


class RuleTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def test_configurables(self):
        example_rule = Rule("test", {"variables": ["one", "sns_topic_arn"]})
        self.assertEqual(example_rule.configurables, ["one"])
