"""Parses reflex config file to be used by application."""
import logging

from reflex_cli.config_parser import ConfigParser
from reflex_cli.reflex_github import ReflexGithub
from reflex_cli.reflex_initializer import ReflexInitializer

LOGGER = logging.getLogger("reflex_cli")


class ConfigVersionUpdater:
    """Checks remote sources for newer measure releases"""

    def __init__(self, config_file, select_all):

        self.select_all = select_all
        self.config_file = config_file
        self.current_config = ConfigParser(
            self.config_file
        ).parse_valid_config()
        self.current_measures = self._collect_measures()

    def _collect_measures(self):
        """Pulls out all measure names for a config file."""
        measure_list = []
        for measure in self.current_config["measures"]:
            measure_list.append(list(measure)[0])
        return measure_list

    def gather_latest_remote_versions(self):
        """Reaches out to urls to get tag information per rule."""
        remote_versions = {}
        for measure_dict in self.current_config["measures"]:
            measure = list(measure_dict)[0]
            remote_url = self._find_measure_value(measure, "url")
            if not remote_url:
                remote_url = "https://github.com/cloudmitigator/" + measure
            LOGGER.debug("Measure: %s has remote: %s", measure, remote_url)
            remote_versions[measure] = ReflexGithub().get_remote_version(
                self._get_repo_format(remote_url)
            )
            LOGGER.debug(
                "Measure has remote version: %s", remote_versions[measure]
            )
        return remote_versions

    def _find_measure_value(self, measure_name, key):
        for measure in self.current_config["measures"]:
            if measure.get(measure_name):
                return measure.get(measure_name).get(key)
        return None

    def _set_measure_value(self, measure_name, key, value):
        """Overwrites existing key with value."""
        for measure in self.current_config["measures"]:
            if measure.get(measure_name):
                measure[measure_name][key] = value

    @staticmethod
    def _get_repo_format(remote):
        """Takes in a repo URL and returns its repo format."""
        org_repo_string = None
        github_string = remote.find("github.com/")
        if github_string > 0:
            org_repo_string = "/".join(
                remote[github_string + 11 :].split("/")  # noqa: E203
            )
        LOGGER.debug("Found repo string to be: %s", org_repo_string)
        return org_repo_string

    def compare_current_rule_versions(self):
        """Iterates over all rules and compares rules with remote versions."""
        LOGGER.debug("Comparing current rule versions.")
        remote_versions = self.gather_latest_remote_versions()
        for measure_dict in self.current_config["measures"]:
            measure = list(measure_dict)[0]
            current_version = self._find_measure_value(measure, "version")
            remote_version = remote_versions[measure]
            if not remote_version:
                LOGGER.debug(
                    "No release information for %s. Skipping!", measure
                )
                continue
            if current_version != remote_version:
                LOGGER.info(
                    "%s (current version: %s) has new release: %s.",
                    measure,
                    current_version,
                    remote_version,
                )
                if self.select_all or self.verify_upgrade_interest():
                    self._set_measure_value(measure, "version", remote_version)

    @staticmethod
    def verify_upgrade_interest():
        """Prompts user whether or not they want to upgrade rule."""
        verify = input("Upgrade? (y/n):")
        return verify.lower() == "y"

    def overwrite_reflex_config(self):
        """If any upgrades possible, overwrite current reflex config."""
        initializer = ReflexInitializer(self.config_file, False)
        initializer.config_file = self.config_file
        initializer.configs = self.current_config
        initializer.write_config_file()
