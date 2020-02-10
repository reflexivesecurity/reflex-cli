import os
import unittest

from reflex_cli.config_version_updater import ConfigVersionUpdater


class ConfigVersionUpdaterTestCase(unittest.TestCase):
    def setUp(self):
        self.test_config_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/reflex.yaml")
        )
        self.test_config_updater = ConfigVersionUpdater(self.test_config_file)

    def test_collect_measures(self):
        current_measures = self.test_config_updater.current_measures
        self.assertTrue(isinstance(current_measures, list))
        self.assertEqual("aws-detect-root-user-activity", current_measures[0])

    def test_gather_latest_remote_versions(self):
        latest_versions = (
            self.test_config_updater.gather_latest_remote_versions()
        )
        measure_keys = self.test_config_updater.current_config["measures"]
        print(measure_keys)
        self.assertTrue(isinstance(latest_versions, dict))
        self.assertEqual(measure_keys, latest_versions.keys())
