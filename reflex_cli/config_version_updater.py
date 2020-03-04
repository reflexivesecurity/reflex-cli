"""Parses reflex config file to be used by application."""
import logging

from reflex_cli.config_parser import ConfigParser
from reflex_cli.reflex_github import ReflexGithub
from reflex_cli.reflex_initializer import ReflexInitializer

LOGGER = logging.getLogger("reflex_cli")


class ConfigVersionUpdater:
    """Checks remote sources for newer rule releases"""

    def __init__(self, config_file, select_all):

        self.select_all = select_all
        self.config_file = config_file
        self.current_config = ConfigParser(
            self.config_file
        ).parse_valid_config()
        self.current_rules = self._collect_rules()

    def _collect_rules(self):
        """Pulls out all rule names for a config file."""
        rule_list = []
        for rule in self.current_config["rules"]:
            rule_list.append(list(rule)[0])
        return rule_list

    def gather_latest_remote_versions(self):
        """Reaches out to urls to get tag information per rule."""
        remote_versions = {}
        for rule_dict in self.current_config["rules"]:
            rule = list(rule_dict)[0]
            remote_url = self._find_rule_value(rule, "url")
            if not remote_url:
                remote_url = "https://github.com/cloudmitigator/" + rule
            LOGGER.debug("Rule: %s has remote: %s", rule, remote_url)
            remote_versions[rule] = ReflexGithub().get_remote_version(
                self._get_repo_format(remote_url)
            )
            LOGGER.debug("rule has remote version: %s", remote_versions[rule])
        return remote_versions

    def _find_rule_value(self, rule_name, key):
        for rule in self.current_config["rules"]:
            if rule.get(rule_name):
                return rule.get(rule_name).get(key)
        return None

    def _set_rule_value(self, rule_name, key, value):
        """Overwrites existing key with value."""
        for rule in self.current_config["rules"]:
            if rule.get(rule_name):
                rule[rule_name][key] = value

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
        for rule_dict in self.current_config["rules"]:
            rule = list(rule_dict)[0]
            current_version = self._find_rule_value(rule, "version")
            remote_version = remote_versions[rule]
            if not remote_version:
                LOGGER.debug("No release information for %s. Skipping!", rule)
                continue
            if current_version != remote_version:
                LOGGER.info(
                    "%s (current version: %s) has new release: %s.",
                    rule,
                    current_version,
                    remote_version,
                )
                if self.select_all or self.verify_upgrade_interest():
                    self._set_rule_value(rule, "version", remote_version)

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
