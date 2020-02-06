import unittest
from unittest.mock import MagicMock

from reflex_cli.measure_discoverer import MeasureDiscoverer


class MeasureDiscovererTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.discoverer = MeasureDiscoverer()
        self.org_api_mock = MagicMock()
        self.repo_mock1 = MagicMock()
        self.repo_mock1.name = "reflex-aws-test"
        self.repo_mock2 = MagicMock()
        self.repo_mock2.name = "reflex-test"
        self.org_api_mock.get_repos.return_value = [
            self.repo_mock1,
            self.repo_mock2,
        ]
        self.discoverer.github_client.get_organization = MagicMock(
            return_value=self.org_api_mock
        )

    def test_is_rule_repository(self):
        self.assertTrue(self.discoverer.is_rule_repository("reflex-aws-test"))
        self.assertFalse(self.discoverer.is_rule_repository("aws-test"))

    def test_filter_reflex_repos(self):
        filtered_repos = self.discoverer.filter_reflex_repos(self.org_api_mock)
        self.assertEqual(filtered_repos[0].name, "reflex-aws-test")
        self.assertEqual(len(filtered_repos), 1)

    def test_collect_measures(self):
        self.assertEqual(self.discoverer.discovered_measures, {})

        mocked_measures = {"cloudmitigator": [self.repo_mock1]}
        self.discoverer.collect_measures()

        self.assertEqual(self.discoverer.discovered_measures, mocked_measures)