import unittest
from reflex_cli.measure_discoverer import MeasureDiscoverer


class MeasureDiscovererTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.discoverer = MeasureDiscoverer()

    def test_is_rule_repository(self):
        self.assertTrue(self.discoverer.is_rule_repository("reflex-aws-test"))
        self.assertFalse(self.discoverer.is_rule_repository("aws-test"))
