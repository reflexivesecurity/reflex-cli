"""Parses reflex config file to be used by application."""
import logging
import os

from reflex_cli.config_parser import ConfigParser

LOGGER = logging.getLogger("reflex_cli")


class ConfigVersionUpdater:
    """Creates assets required to build a reflex deployment."""

    def __init__(self, context):
        self.config_file = os.path.abspath(
            os.path.join(context.home), "reflex.yaml"
        )
        self.current_config = ConfigParser(
            self.config_file
        ).parse_valid_config()

    def compare_current_rule_versions(self):
        """Iterates over all rules and compares rules with remote versions."""

    def gather_latest_remote_versions(self):
        """Reaches out to urls to get tag information per rule."""

    def verify_upgrade_interest(self):
        """Prompts user whether or not they want to upgrade rule."""

    def overwrite_reflex_config(self):
        """If any upgrades possible, overwrite current reflex config."""
