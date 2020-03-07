"""Holder of template generation logic"""
import logging

import requests
import yaml
from reflex_cli.rule import Rule

LOGGER = logging.getLogger("reflex_cli")

RULE_MANIFEST_ENDPOINT = "http://manifest.cloudmitigator.com"


class RuleDiscoverer:
    """Discovers rules by querying github remotes."""

    def __init__(self):
        self.discovered_rules = []

    def collect_rules(self):  # pragma: no cover
        """Collects a list of repos that match rules."""
        raw_rules = self.pull_manifest_content()
        yaml_rules = yaml.load(raw_rules, Loader=yaml.SafeLoader)
        self.discovered_rules = self.create_rule_list(yaml_rules["rules"])
        return self.discovered_rules

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
        raw_rules_response = requests.get(RULE_MANIFEST_ENDPOINT)
        return raw_rules_response.content

    def display_discovered_rules(self):  # pragma: no cover
        """Method outputs rule information in a usable fashion"""
        LOGGER.info("Rules discovered in CloudMitigator Github organization.")
        LOGGER.info("-------------------------------------------")
        for rule in self.discovered_rules:
            LOGGER.info(
                "\033[4m%s\033[0m: \n\t\033[4mDescription\033[0m:"
                " %s\n\t\033[4mLatest release\033[0m: %s\n",
                rule.name,
                rule.description,
                rule.version,
            )
