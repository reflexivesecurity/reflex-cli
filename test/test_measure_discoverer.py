import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.measure_discoverer import MeasureDiscoverer


class MeasureDiscovererTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.discoverer = MeasureDiscoverer()
        self.git_repos_mock = MagicMock()
        self.repo_mock1 = MagicMock()
        self.repo_mock1.name = "reflex-aws-test"
        self.repo_mock2 = MagicMock()
        self.repo_mock2.name = "reflex-test"

    def test_is_rule_repository(self):
        self.assertTrue(self.discoverer.is_rule_repository("reflex-aws-test"))
        self.assertFalse(self.discoverer.is_rule_repository("aws-test"))

    @patch("reflex_cli.reflex_github.ReflexGithub.get_remote_version")
    def test_filter_reflex_repos(self, mock_remote):
        mock_remote.return_value = "v0.0.0"
        repos = [self.repo_mock1, self.repo_mock2]
        filtered_repos = self.discoverer.filter_reflex_repos(repos)
        self.assertEqual(filtered_repos[0].name, "reflex-aws-test")
        self.assertEqual(len(filtered_repos), 1)

    @patch("reflex_cli.reflex_github.ReflexGithub.get_repos")
    @patch("reflex_cli.reflex_github.ReflexGithub.get_remote_version")
    def test_collect_measures(self, mock_get_remote_version, mock_get_repos):
        test_discoverer = MeasureDiscoverer()
        mock_get_remote_version.return_value = "v0.0.0"
        mock_get_repos.return_value = [self.repo_mock1, self.repo_mock2]
        self.assertEqual(test_discoverer.discovered_measures, [])

        mocked_measures = [self.repo_mock1]
        self.discoverer.collect_measures()

        self.assertEqual(self.discoverer.discovered_measures, mocked_measures)
