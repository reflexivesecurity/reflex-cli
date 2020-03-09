"""Parses reflex config file to be used by application."""
import logging

from reflex_cli.config_parser import ConfigParser
from reflex_cli.reflex_github import ReflexGithub
from reflex_cli.reflex_initializer import ReflexInitializer
from reflex_cli.rule_discoverer import RuleDiscoverer
from reflex_cli.user_input import UserInput

LOGGER = logging.getLogger("reflex_cli")


class ConfigVersionUpdater:
    """Checks remote sources for newer rule releases"""

    def __init__(self, config_file, select_all):

        self.user_input = UserInput(select_all)
        self.config_file = config_file
        self.current_config = ConfigParser(self.config_file)
        self.current_config.parse_valid_config()

    def gather_latest_remote_versions(self):
        """Reaches out to urls to get tag information per rule."""
        manifest_rules = RuleDiscoverer().collect_rules()
        remote_versions = {}
        for rule in self.current_config.rule_list:
            remote_url = self._find_rule_value(rule.name, "url")
            if not remote_url:
                for manifest_rule in manifest_rules:
                    if manifest_rule.name == rule.name:
                        remote_versions[rule.name] = manifest_rule.version
            else:
                LOGGER.debug("Rule: %s has remote: %s", rule, remote_url)
                remote_versions[rule.name] = ReflexGithub().get_remote_version(
                    ReflexGithub.get_repo_format(remote_url)
                )
            LOGGER.debug(
                "rule has remote version: %s", remote_versions[rule.name]
            )
        return remote_versions

    def _find_rule_value(self, rule_name, key):
        for rule in self.current_config.raw_configuration["rules"]:
            if rule.get(rule_name):
                return rule.get(rule_name).get(key)
        return None

    def _set_rule_value(self, rule_name, key, value):
        """Overwrites existing key with value."""
        for rule in self.current_config.raw_configuration["rules"]:
            if rule.get(rule_name):
                rule[rule_name][key] = value

    def compare_current_rule_versions(self):
        """Iterates over all rules and compares rules with remote versions."""
        LOGGER.debug("Comparing current rule versions.")
        remote_versions = self.gather_latest_remote_versions()
        for rule in self.current_config.rule_list:
            current_version = self._find_rule_value(rule.name, "version")
            remote_version = remote_versions[rule.name]
            if not remote_version:
                LOGGER.debug(
                    "No release information for %s. Skipping!", rule.name
                )
                continue
            if current_version != remote_version:
                LOGGER.info(
                    "%s (current version: %s) has new release: %s.",
                    rule.name,
                    current_version,
                    remote_version,
                )
                if self.user_input.verify_upgrade_interest():
                    self._set_rule_value(rule.name, "version", remote_version)

    def overwrite_reflex_config(self):
        """If any upgrades possible, overwrite current reflex config."""
        initializer = ReflexInitializer(self.config_file, False)
        initializer.config_file = self.config_file
        initializer.configs = self.current_config.raw_configuration
        initializer.write_config_file()
