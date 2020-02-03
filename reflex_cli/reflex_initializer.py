"""Parses reflex config file to be used by application."""
import logging
import os

import pkg_resources
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

TEMPLATE_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "templates")
)

LOGGER = logging.getLogger("reflex_cli")


class ReflexInitializer:
    """Creates assets required to build a reflex deployment."""

    def __init__(self, home_directory):
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
    def query_possible_measures():
        """Iterates over templates and gets confirmation per measure."""
        possible_measures = []
        for filename in os.listdir(TEMPLATE_FOLDER):
            if filename.endswith(".tf"):
                confirm = input(f"{filename}? (Yy/Nn):")
                if confirm.lower() == "y":
                    possible_measures.append(filename[:-3])
        LOGGER.debug("Measures selected for config: %s", possible_measures)
        return possible_measures

    def determine_config_values(self):
        """Outlines keys of config file and gathers values."""
        package_object = pkg_resources.require("reflex-cli")[0]
        self.configs["version"] = package_object.version
        LOGGER.debug("Reflex version set to: %s", self.configs["version"])
        self.configs["default_notification_email"] = input("Default email:")
        self.configs["providers"] = ["aws"]
        self.configs["measures"] = self.query_possible_measures()

    def render_template(self):
        """Renders jinja2 template with yaml dumps."""
        version_dump = yaml.dump({"version": self.configs["version"]})
        default_notification_email_dump = yaml.dump(
            {
                "default_notification_email": self.configs[
                    "default_notification_email"
                ]
            }
        )
        providers_dump = yaml.dump({"providers": self.configs["providers"]})
        measures_dump = yaml.dump({"measures": self.configs["measures"]})
        template = self.template_env.get_template("reflex.yaml.jinja2")
        rendered_template = template.render(
            default_email=default_notification_email_dump,
            providers=providers_dump,
            measures=measures_dump,
            version=version_dump,
        )
        LOGGER.debug("Config template rendered as: %s", rendered_template)
        return rendered_template

    def write_config_file(self):
        """Opens config file, dumps dict as yaml."""
        LOGGER.debug("Writing config file to: %s", self.config_file)
        with open(self.config_file, "w") as config_file:
            config_file.write(self.render_template())
