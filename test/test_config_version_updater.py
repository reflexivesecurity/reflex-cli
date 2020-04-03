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

    def test_find_rule_value(self):
        real_value = self.test_config_updater._find_rule_value(
            "aws-detect-root-user-activity", "version"
        )
        self.assertEqual(real_value, "v0.0.1")
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
            "aws-detect-root-user-activity", "version", "v0.0.1"
        )

    @patch("reflex_cli.config_version_updater.RuleDiscoverer.collect_rules")
    def test_gather_latest_remote_versions(self, rule_mock):
        rule_list_mock = MagicMock()
        rule_list_mock.name = "aws-detect-root-user-activity"
        rule_list_mock.version = "v0.0.1"
        collect_rule_mock = MagicMock()
        collect_rule_mock.name = "reflex-aws-aws-detect-root-user-activity"
        collect_rule_mock.version = "v0.0.1"
        rule_mock.return_value = [collect_rule_mock]
        self.test_config_updater.current_config.rule_list = [rule_list_mock]
        latest_versions = (
            self.test_config_updater.gather_latest_remote_versions()
        )
        self.assertTrue(isinstance(latest_versions, dict))
        self.assertEqual(
            latest_versions["aws-detect-root-user-activity"], "v0.0.1"
        )

    @patch(
        "reflex_cli.config_version_updater.ConfigVersionUpdater.gather_latest_remote_versions"
    )
    @patch(
        "reflex_cli.config_version_updater.UserInput.verify_upgrade_interest"
    )
    def test_compare_current_rule_versions(
        self, user_input_mock, remote_version_mock
    ):
        rule_list_mock = MagicMock()
        rule_list_mock.name = "aws-detect-root-user-activity"
        rule_list_mock.version = "v0.0.1"
        self.test_config_updater.current_config.rule_list = [rule_list_mock]
        user_input_mock.return_value = True
        remote_version_mock.return_value = {
            "aws-detect-root-user-activity": "v0.0.2"
        }
        self.assertEqual(
            "v0.0.1",
            self.test_config_updater._find_rule_value(
                "aws-detect-root-user-activity", "version"
            ),
        )
        self.test_config_updater.compare_current_rule_versions()
        self.assertEqual(
            "v0.0.2",
            self.test_config_updater._find_rule_value(
                "aws-detect-root-user-activity", "version"
            ),
        )
