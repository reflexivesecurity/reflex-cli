import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.config_version_updater import ConfigVersionUpdater


class ConfigVersionUpdaterTestCase(unittest.TestCase):
    def setUp(self):
        self.test_config_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/reflex.yaml")
        )
        self.test_config_updater = ConfigVersionUpdater(
            self.test_config_file, False
        )

    def test_collect_rules(self):
        current_rules = self.test_config_updater.current_rules
        self.assertTrue(isinstance(current_rules, list))
        self.assertEqual("aws-detect-root-user-activity", current_rules[0])

    def test_find_rule_value(self):
        real_value = self.test_config_updater._find_rule_value(
            "aws-detect-root-user-activity", "version"
        )
        self.assertEqual(real_value, "0.0.1")
        no_value = self.test_config_updater._find_rule_value(
            "aws-detect-root-user-activity", "empty"
        )
        self.assertIsNone(no_value)

    def test_set_rule_value(self):
        self.test_config_updater._set_rule_value(
            "aws-detect-root-user-activity", "version", "invalid"
        )
        new_value = self.test_config_updater._find_rule_value(
            "aws-detect-root-user-activity", "version"
        )
        self.assertEqual(new_value, "invalid")
        self.test_config_updater._set_rule_value(
            "aws-detect-root-user-activity", "version", "0.0.1"
        )

    def test_get_repo_format(self):
        repo_string = self.test_config_updater._get_repo_format(
            "http://github.com/test/repository"
        )
        self.assertEqual(repo_string, "test/repository")

        bad_string = self.test_config_updater._get_repo_format(
            "http://githb.com/test/repository"
        )
        self.assertIsNone(bad_string)

    @patch("reflex_cli.config_version_updater.ReflexGithub.get_remote_version")
    def test_gather_latest_remote_versions(self, github_mock):
        github_mock.return_value = "v0.0.1"
        latest_versions = (
            self.test_config_updater.gather_latest_remote_versions()
        )
        self.assertTrue(isinstance(latest_versions, dict))
        self.assertEqual(
            latest_versions["aws-detect-root-user-activity"], "v0.0.1"
        )
