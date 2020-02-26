"""Parses reflex config file to be used by application."""
import logging

import yaml

LOGGER = logging.getLogger("reflex_cli")
REQUIRED_KEYS = ["version"]


class ConfigParser:
    """Parses and validates reflex yaml config file."""

    def __init__(self, config_file):
        self.config_file = config_file
        self.coniguration = {}

    def parse_valid_config(self):
        """Entrypoint to generate and validate config"""
        self.configuration = (  # pylint: disable=attribute-defined-outside-init
            self.generate_config()
        )
        valid_config = self.validate_config(self.configuration)
        if not valid_config:
            raise SystemError(
                f"Invalid configuration file format, config: {self.configuration}"
            )
        return self.configuration

    def generate_config(self):
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
