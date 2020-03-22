"""Class that takes in user input for various CLI pieces"""
import logging
import os

LOGGER = logging.getLogger("reflex_cli")


class UserInput:
    """Class for handling user input."""

    def __init__(self, select_all):
        self.select_all = select_all

    @staticmethod
    def get_input(message):  # pragma: no cover
        """Helper method to return specific input call."""
        return input(message)

    def collect_default_email(self):
        """Collects default email address from user."""
        if self.select_all:
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
            if self.select_all or self.verify_rule(rule):
                LOGGER.info("Adding %s at version %s.", rule.name, rule.version)
                if rule.configurables:
                    configurable_array = []
                    for config in rule.configurables:
                        configurable_array.append(config)
                    possible_rules.append(
                        {
                            rule.name: {
                                "version": rule.version,
                                "configuration": configurable_array,
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
        if not self.select_all:
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
        if not region and not self.select_all:
            region = self.get_input("AWS Region:")
        return region

    def verify_upgrade_interest(self):
        """Prompts user whether or not they want to upgrade rule."""
        if not self.select_all:
            verify = self.get_input("Upgrade? (y/n):")
            return verify.lower() == "y"
        return False
