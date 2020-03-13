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


class ReflexInitializer:
    """Creates assets required to build a reflex deployment."""

    def __init__(self, select_all, config_file):
        self.user_input = UserInput(select_all)
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
        possible_rules = self.user_input.get_rule_input(discovered_rules)
        LOGGER.debug("Rules selected for config: %s", possible_rules)
        return possible_rules

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
        self.configs["rules"] = self.query_possible_rules()

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
        with open(self.config_file, "w") as config_file:
            config_file.write(self.render_template())
