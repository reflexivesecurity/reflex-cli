"""Parses reflex config file to be used by application."""
import logging
import yaml

LOGGER = logging.getLogger("reflex_cli")
REQUIRED_KEYS = ["version"]


class ConfigParser:
    """Parses and validates reflex yaml config file."""

    def __init__(self, config_file):
        self.config_file = config_file

    def generate_config(self):
        """Opens config file, parses yaml, and validates contents."""
        with open(self.config_file, "r") as config_file:
            configuration = yaml.safe_load(config_file)
            LOGGER.debug("Configuration dictionary: %s", configuration)
            self.validate_config(configuration)
        return configuration

    @staticmethod
    def validate_config(config):
        """Validates presence of keys and format of values"""
        for key in REQUIRED_KEYS:
            if key not in list(config):
                raise ValueError(f"{key} was not found in reflex.yaml.")

            if not config[key]:
                raise ValueError(
                    f"{key} was found to have no value in reflex.yaml"
                )
