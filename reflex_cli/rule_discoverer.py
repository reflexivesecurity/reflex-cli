"""Holder of template generation logic"""
import logging
import sys

import requests
import yaml
from reflex_cli.rule import Rule

LOGGER = logging.getLogger("reflex_cli")

RULE_MANIFEST_ENDPOINT = "http://manifest.cloudmitigator.com"


class RuleDiscoverer:
    """Discovers rules by querying github remotes."""

    def __init__(self):
        self.discovered_rules = []
        self.manifest_content = self.pull_manifest_content()
        self.yaml_content = yaml.load(
            self.manifest_content, Loader=yaml.SafeLoader
        )

    def collect_rules(self):  # pragma: no cover
        """Collects a list of repos that match rules."""
        self.discovered_rules = self.create_rule_list(
            self.yaml_content["rules"]
        )
        return self.discovered_rules

    def collect_engine(self):
        """Collects engine configuration from manifest content"""
        return self.yaml_content["engine"]

    @staticmethod
    def create_rule_list(rule_array):
        """Creates rule objects in a list for further ingestion."""
        rule_object_array = []
        for rule in rule_array:
            rule_name = list(rule)[0]
            new_rule = Rule(rule_name, rule[rule_name])
            rule_object_array.append(new_rule)
        return rule_object_array

    @staticmethod
    def pull_manifest_content():  # pragma: no cover
        """Reaches out to manifest endpoint to gather rule information."""
        try:
            raw_rules_response = requests.get(RULE_MANIFEST_ENDPOINT)
        except requests.ConnectionError:
            LOGGER.error(
                "A connection error occurred. Check your internet connection and try again."
            )
            sys.exit(1)
        return raw_rules_response.content

    def display_discovered_rules(self):  # pragma: no cover
        """Method outputs rule information in a usable fashion"""
        LOGGER.info("Rules discovered in CloudMitigator Github organization.")
        LOGGER.info("-------------------------------------------")
        for rule in self.discovered_rules:
            if rule.version:
                LOGGER.info(
                    "\033[4m%s\033[0m: \n\t\033[4mDescription\033[0m:"
                    " %s\n\t\033[4mLatest release\033[0m: %s\n",
                    rule.name,
                    rule.description,
                    rule.version,
                )
