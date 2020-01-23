"""Parses reflex config file to be used by application."""
import yaml


class ConfigParser:
    """Parses and validates reflex yaml config file."""
    def __init__(self, config_file):
        self.config_file = config_file

    def generate_config(self):
        """Opens config file, parses yaml, and validates contents."""
        with open(self.config_file, 'r') as config_file:
            configuration = yaml.safe_load(config_file)
            self.validate_config(configuration)
        return configuration

    def validate_config(self, config):
        """Validates presence of keys and format of values"""
