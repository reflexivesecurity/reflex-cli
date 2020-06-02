"""Class that takes in user input for various CLI pieces"""
import logging
import os

from PyInquirer import prompt

LOGGER = logging.getLogger("reflex_cli")
HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


class UserInput:
    """Class for handling user input."""

    def __init__(self, interactive):
        self.interactive = interactive

    @staticmethod
    def get_input(message):  # pragma: no cover
        """Helper method to return specific input call."""
        return input(message)

    def collect_default_email(self):
        """Collects default email address from user."""
        if not self.interactive:
            return "placeholder@example.com"
        return self.get_input("Default email:")

    def verify_rule(self, rule):
        """Gets user input about rule inclusion."""
        verify_string = f"Add {rule.name} at version {rule.version}?"
        rule_input = self.get_input(verify_string + " (Yy/Nn):")
        return rule_input.lower() == "y"

    def get_rule_input(self, discovered_rules):
        """Iterates over all rules and verifies inputs."""
        possible_rules = []
        for rule in discovered_rules:
            if rule.version is None:
                continue
            if not self.interactive or self.verify_rule(rule):
                LOGGER.info(
                    "✅ Adding %s%s%s%s at version %s%s%s",
                    OKGREEN,
                    BOLD,
                    rule.name,
                    ENDC,
                    OKBLUE,
                    rule.version,
                    ENDC,
                )
                if rule.configurables:
                    configurable_dict = {}
                    for config in rule.configurables:
                        LOGGER.debug(
                            "Adding element %s to config array.", config
                        )
                        if isinstance(config, str):
                            configurable_dict[config] = ""
                        elif isinstance(config, dict):
                            config_key = list(config)[0]
                            configurable_dict[config_key] = config[config_key]
                    possible_rules.append(
                        {
                            rule.name: {
                                "version": rule.version,
                                "configuration": configurable_dict,
                            }
                        }
                    )
                else:
                    possible_rules.append(
                        {rule.name: {"version": rule.version}}
                    )
        return possible_rules

    def collect_backend_key_values(self):  # pragma: no cover
        """Continually collects backend config key value pairs from user."""
        more_config = True
        key_value_array = []
        while more_config:
            config_key = self.get_input("Backend configuration key: ")
            config_value = self.get_input("Backend configuration value: ")
            key_value_array.append({config_key: config_value})
            continue_config = self.get_input(
                "Add more configurations? (Yy/Nn):"
            )
            more_config = continue_config.lower() == "y"
        return key_value_array

    def get_backend_configuration(self):  # pragma: no cover
        """Collects backend configuration information."""
        if self.interactive:
            backend_verify = self.get_input("Configure backend? (Yy/Nn): ")
            if backend_verify.lower() != "y":
                return ""
            LOGGER.info(
                "Collecting backend configuration. To see key value configuration,"
                " check out https://www.terraform.io/docs/backends/index.html."
            )
            backend_type = self.get_input("Backend type?: ")
            backend_config = {backend_type: self.collect_backend_key_values()}
            return backend_config
        return None

    def get_region(self):
        """Either sets region via environment variable or input."""
        region = os.environ.get("AWS_REGION")
        if not region and self.interactive:
            region = self.get_input("AWS Region:")
        return region

    @staticmethod
    def ask_to_overwrite(file_path):
        """Asks user whether to allow overwrite file. """
        configuration_overwrite = [
            {
                "type": "confirm",
                "message": f"Configuration file found at {file_path}, overwrite?",
                "name": "overwrite_configuration",
                "default": False,
            }
        ]
        overwrite = prompt(configuration_overwrite)
        return overwrite["overwrite_configuration"]

    def verify_upgrade_interest(self):
        """Prompts user whether or not they want to upgrade rule."""
        if self.interactive:
            verify = self.get_input("Upgrade? (y/n):")
            return verify.lower() == "y"
        return False
