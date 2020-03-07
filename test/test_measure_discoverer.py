import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.rule_discoverer import RuleDiscoverer


class RuleDiscovererTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.discoverer = RuleDiscoverer()

    def test_create_rule_list(self):
        test_rules = [{"test-rule": {"description": "example"}}]
        rule_objects = self.discoverer.create_rule_list(test_rules)
        self.assertEqual(rule_objects[0].name, "test-rule")
