"""Parses reflex config file to be used by application."""
import logging
import os

import pkg_resources

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
from reflex_cli.rule_discoverer import RuleDiscoverer
from reflex_cli.user_input import UserInput

TEMPLATE_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "templates")
)

LOGGER = logging.getLogger("reflex_cli")

REFLEX_PREFIX = "reflex-aws-"


class ReflexInitializer:
    """Creates assets required to build a reflex deployment."""

    def __init__(self, interactive, config_file):
        self.user_input = UserInput(interactive)
        self.configs = {}
        self.config_file = config_file
        self.rule_discoverer = RuleDiscoverer()
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates"),
            autoescape=select_autoescape(["jinja2"]),
        )

    def query_possible_rules(self):
        """Iterates over templates and gets confirmation per rule."""
        discovered_rules = self.rule_discoverer.collect_rules()
        raw_rules = self.user_input.get_rule_input(discovered_rules)
        LOGGER.debug("Rules selected for config: %s", raw_rules)
        possible_rules = self.strip_rule_common_names(raw_rules)
        return possible_rules

    @staticmethod
    def strip_rule_common_names(rule_array):
        """Takes in array of rules and strips out common repo prefix."""
        stripped_array = []
        for rule in rule_array:
            rule_key = list(rule.keys())[0]
            stripped_key = rule_key.replace(REFLEX_PREFIX, "")
            new_rule = {stripped_key: rule[rule_key]}
            stripped_array.append(new_rule)
        return stripped_array

    @staticmethod
    def get_reflex_version():
        """Looks at package version of CLI to determine reflex version."""
        package_object = pkg_resources.require("reflex-cli")[0]
        LOGGER.debug("Reflex version found as: %s", package_object.version)
        return package_object.version

    def get_engine_version(self):
        """Pulls the engine version information from discoverer."""
        engine_dictionary = self.rule_discoverer.collect_engine()
        return engine_dictionary["reflex-engine"]["version"]

    def set_global_values(self):
        """Sets values for common configurations across guardrails."""
        global_dict = {}
        global_dict["default_email"] = self.user_input.collect_default_email()
        return global_dict

    def determine_config_values(self):  # pragma: no cover
        """Outlines keys of config file and gathers values."""
        self.configs["cli_version"] = self.get_reflex_version()
        self.configs["engine_version"] = self.get_engine_version()
        self.configs["globals"] = self.set_global_values()
        self.configs["providers"] = [
            {"aws": {"region": self.user_input.get_region()}}
        ]
        self.configs["backend"] = self.user_input.get_backend_configuration()
        self.configs["rules"] = {"aws": self.query_possible_rules()}

    def render_template(self):  # pragma: no cover
        """Renders jinja2 template with yaml dumps."""
        version_dump = yaml.dump(
            {"cli_version": ("%s" % self.configs["cli_version"])}
        )
        engine_dump = yaml.dump(
            {"engine_version": ("%s" % self.configs["engine_version"])}
        )
        globals_dump = yaml.dump({"globals": self.configs["globals"]})
        providers_dump = yaml.dump({"providers": self.configs["providers"]})
        rules_dump = yaml.dump({"rules": self.configs["rules"]})
        backend_dump = yaml.dump({"backend": self.configs["backend"]})

        template = self.template_env.get_template("reflex.yaml.jinja2")
        rendered_template = template.render(
            global_configs=globals_dump,
            providers=providers_dump,
            backend=backend_dump,
            rules=rules_dump,
            version=version_dump,
            engine=engine_dump,
        )
        LOGGER.debug("Config template rendered as: %s", rendered_template)
        return rendered_template

    def write_config_file(self):  # pragma: no cover
        """Opens config file, dumps dict as yaml."""
        LOGGER.debug("Writing config file to: %s", self.config_file)
        if os.path.exists(self.config_file):
            write_file = self.user_input.ask_to_overwrite(self.config_file)
        else:
            write_file = True
        if write_file:
            with open(self.config_file, "w") as config_file:
                config_file.write(self.render_template())
