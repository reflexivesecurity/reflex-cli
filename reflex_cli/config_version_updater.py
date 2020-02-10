"""Parses reflex config file to be used by application."""
import logging
import os

import github
from reflex_cli.config_parser import ConfigParser

LOGGER = logging.getLogger("reflex_cli")


class ConfigVersionUpdater:
    """Creates assets required to build a reflex deployment."""

    def __init__(self, config_file):

        if os.environ.get("REFLEX_GITHUB_TOKEN"):
            self.github_client = github.Github(
                os.environ.get("REFLEX_GITHUB_TOKEN")
            )
        else:
            self.github_client = github.Github()

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
        for measure in self.current_measures:
            remote_url = self._find_measure_value(measure, "url")
            if not remote_url:
                remote_url = "https://github.com/cloudmitigator/" + measure
            remote_versions[measure] = self.get_remote_version(
                self._get_repo_format(remote_url)
            )
        return remote_versions

    def _find_measure_value(self, measure_name, key):
        for measure in self.current_config["measures"]:
            if measure.get(measure_name):
                return measure.get(measure_name).get(key)
        return None

    def _set_measure_value(self, measure_name, key, value):
        return None

    def get_remote_version(self, remote):
        repo = self.github_client.get_repo(remote)
        latest_release = repo.get_latest_release()
        return latest_release.tag_name

    def _get_repo_format(self, remote):
        """Takes in a repo URL and returns its repo format."""
        org_repo_string = None
        github_string = remote.find("github.com/")
        if github_string > 0:
            org_repo_string = "/".join(remote[github_string + 11].split("/"))
        return org_repo_string

    def compare_current_rule_versions(self):
        """Iterates over all rules and compares rules with remote versions."""
        remote_versions = self.gather_latest_remote_versions()
        for measure in self.current_measures:
            current_version = self._find_measure_value(measure, "version")
            remote_version = remote_versions[measure]
            if current_version != remote_version:
                if self.verify_upgrade_interest(
                    measure, current_version, remote_version
                ):
                    self._set_measure_value(measure, "version", remote_version)

    def verify_upgrade_interest(self, measure, current, remote):
        """Prompts user whether or not they want to upgrade rule."""
        verify = input(
            "%s (current version: %s) has new release: %s. Upgrade? (y/n):"
            % measure,
            current,
            remote,
        )
        return verify.lower() == "y"

    def overwrite_reflex_config(self):
        """If any upgrades possible, overwrite current reflex config."""
