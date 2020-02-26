"""Parses reflex config file to be used by application."""
import logging
import os

import pkg_resources

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
from reflex_cli.measure_discoverer import MeasureDiscoverer

TEMPLATE_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "templates")
)

LOGGER = logging.getLogger("reflex_cli")


class ReflexInitializer:
    """Creates assets required to build a reflex deployment."""

    def __init__(self, home_directory, select_all):
        self.select_all = select_all
        self.home_directory = home_directory
        self.configs = {}
        self.config_file = os.path.abspath(
            os.path.join(self.home_directory, "reflex.yaml")
        )
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates"),
            autoescape=select_autoescape(["jinja2"]),
        )

    @staticmethod
    def get_input(message):
        """Helper method to return specific input call."""
        return input(message)

    def query_possible_measures(self):
        """Iterates over templates and gets confirmation per measure."""
        possible_measures = []
        discovered_measures = MeasureDiscoverer().collect_measures()

        for measure in discovered_measures:
            if measure.version is None:
                continue
            verify_string = f"Add {measure.name} at version {measure.version}?"

            if self.select_all:
                LOGGER.info(
                    "Adding %s at version %s.", measure.name, measure.version
                )
                possible_measures.append(
                    {measure.name: {"version": measure.version}}
                )
            elif self.get_input(verify_string + " (Yy/Nn):").lower() == "y":
                possible_measures.append(
                    {measure.name: {"version": measure.version}}
                )
        LOGGER.debug("Measures selected for config: %s", possible_measures)
        return possible_measures

    def set_version(self):
        """Looks at package version of CLI to determine reflex version."""
        package_object = pkg_resources.require("reflex-cli")[0]
        self.configs["version"] = package_object.version
        LOGGER.debug("Reflex version set to: %s", self.configs["version"])

    def determine_config_values(self):  # pragma: no cover
        """Outlines keys of config file and gathers values."""
        self.set_version()
        if self.select_all:
            self.configs["default_email"] = "placeholder@example.com"
        else:
            self.configs["default_email"] = self.get_input("Default email:")
        region = os.environ.get("AWS_REGION")
        if not region:
            region = self.get_input("AWS Region:")
        self.configs["providers"] = [{"aws": {"region": region}}]
        self.configs["measures"] = self.query_possible_measures()

    def render_template(self):  # pragma: no cover
        """Renders jinja2 template with yaml dumps."""
        version_dump = yaml.dump({"version": self.configs["version"]})
        default_email_dump = yaml.dump(
            {"default_email": self.configs["default_email"]}
        )
        providers_dump = yaml.dump({"providers": self.configs["providers"]})
        measures_dump = yaml.dump({"measures": self.configs["measures"]})

        template = self.template_env.get_template("reflex.yaml.jinja2")
        rendered_template = template.render(
            default_email=default_email_dump,
            providers=providers_dump,
            measures=measures_dump,
            version=version_dump,
        )
        LOGGER.debug("Config template rendered as: %s", rendered_template)
        return rendered_template

    def write_config_file(self):  # pragma: no cover
        """Opens config file, dumps dict as yaml."""
        LOGGER.debug("Writing config file to: %s", self.config_file)
        with open(self.config_file, "w") as config_file:
            config_file.write(self.render_template())
