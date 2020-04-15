"""Parses reflex config file to be used by application."""
import logging
import sys

# pylint: disable=wrong-import-order
import yaml
from reflex_cli.rule import Rule
from yaml.constructor import SafeConstructor

LOGGER = logging.getLogger("reflex_cli")
REQUIRED_KEYS = [
    "cli_version",
    "globals",
    "rules",
    "providers",
    "backend",
    "engine_version",
]


def add_bool(self, node):
    """Allows bools to be set as strings."""
    return self.construct_scalar(node)


SafeConstructor.add_constructor("tag:yaml.org,2002:bool", add_bool)


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
            LOGGER.info(
                "Invalid configuration file format found at %s",
                self.config_file,
            )
            sys.exit(55)

    def create_rule_list(self):
        """Creates rule objects in a list for further ingestion."""
        rule_object_array = []
        try:
            for rule in self.raw_configuration["rules"]["aws"]:
                rule_name = list(rule)[0]
                new_rule = Rule(rule_name, rule[rule_name])
                rule_object_array.append(new_rule)
            return rule_object_array
        except KeyError:
            LOGGER.info(
                "Parsing config failed: Incorrect configuration"
                " rule structure in %s",
                self.config_file,
            )
            sys.exit(55)

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
            elif not config[key] and key != "backend":
                LOGGER.info("Key %s has no value in reflex.yaml", key)
                valid = False
        return valid
