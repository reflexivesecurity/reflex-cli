"""Parses reflex config file to be used by application."""
import logging

import yaml
from reflex_cli.rule import Rule

LOGGER = logging.getLogger("reflex_cli")
REQUIRED_KEYS = ["cli_version"]


class ConfigParser:
    """Parses and validates reflex yaml config file."""

    def __init__(self, config_file):
        self.config_file = config_file
        self.raw_coniguration = {}
        self.rule_list = []

    def parse_valid_config(self):
        """Entrypoint to generate and validate config"""
        self.raw_configuration = (  # pylint: disable=attribute-defined-outside-init
            self.parse_yaml_config()
        )
        self.rule_list = self.create_rule_list()
        valid_config = self.validate_config(self.raw_configuration)
        if not valid_config:
            raise SystemError(
                f"Invalid configuration file format, config: {self.raw_configuration}"
            )

    def create_rule_list(self):
        """Creates rule objects in a list for further ingestion."""
        rule_object_array = []
        for rule in self.raw_configuration["rules"]:
            rule_name = list(rule)[0]
            new_rule = Rule(rule_name, rule[rule_name])
            rule_object_array.append(new_rule)
        return rule_object_array

    def parse_yaml_config(self):
        """Opens config file, parses yaml."""
        with open(self.config_file, "r") as config_file:
            configuration = yaml.safe_load(config_file)
            LOGGER.debug("Configuration dictionary: %s", configuration)
        return configuration

    @staticmethod
    def validate_config(config):
        """Validates presence of keys and format of values"""
        valid = True
        config_list = list(config)

        for key in REQUIRED_KEYS:
            if key not in config_list:
                LOGGER.info("Key %s was not found in reflex.yaml.", key)
                valid = False
            elif not config[key]:
                LOGGER.info("Key %s has no value in reflex.yaml", key)
                valid = False

        return valid
