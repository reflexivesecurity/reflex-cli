import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.reflex_github import ReflexGithub


class ReflexGithubTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def test_get_repo_format(self):
        repo_string = ReflexGithub.get_repo_format(
            "http://github.com/test/repository"
        )
        self.assertEqual(repo_string, "test/repository")

        bad_string = ReflexGithub.get_repo_format(
            "http://githb.com/test/repository"
        )
        self.assertIsNone(bad_string)

    # def setUp(self):
    #     self.client = ReflexGithub()


#    @patch("reflex_cli.reflex_github.github.Github")
#    def test_get_repos_calls_organization_get_repos(self, mock_github):
#        """ Tests that get_repos calls the GitHub api get_repos function """
#        get_repos = MagicMock()
#        get_organizations = MagicMock()
#        get_organizations.get_repos.return_value = get_repos
#        mock_github.return_value = get_organizations
#        client = ReflexGithub()
#        client.get_repos()
#        mock_github.get_repos.assert_called_once()
#
# def test_get_remote_version_returns_none_no(self):
#     self.assertTrue(self.discoverer.is_rule_repository("reflex-aws-test"))
#     self.assertFalse(self.discoverer.is_rule_repository("aws-test"))
