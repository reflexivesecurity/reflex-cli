"""Holder of template generation logic"""
import logging
import os
from pathlib import Path

import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape

LOGGER = logging.getLogger("reflex_cli")


class TemplateGenerator:
    """Generate a set of templates from a given config."""

    def __init__(self, configuration, output_directory):
        self.configuration = configuration
        self.output_directory = output_directory
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates"),
            autoescape=select_autoescape(["tf"]),
        )
        self.default_email = self.configuration["default_notification_email"]
        self._ensure_output_directory_exists()

    def _ensure_output_directory_exists(self):
        """Ensure that the path to the output directory exists."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)

    def create_templates(self):
        """Generates templates for every measure in configuration."""
        for measure in self.configuration["measures"]:
            template_name = self.determine_template_name(measure)
            LOGGER.debug("Rendering template with name: %s", template_name)
            rendered_template = self.generate_template(template_name)
            if rendered_template:
                self.write_template_file(template_name, rendered_template)

    @staticmethod
    def determine_template_name(measure):
        """Inspects instance type of measure to determine file name."""
        if isinstance(measure, str):
            template_name = measure + ".tf"
        elif isinstance(measure, dict):
            template_name = list(measure)[0] + ".tf"
        return template_name

    def write_template_file(self, template_name, rendered_template):
        """Writes output of rendering to file"""
        output_file = os.path.join(self.output_directory, template_name)
        LOGGER.debug("Writing template file to: %s", output_file)
        with open(output_file, "w+") as file_handler:
            file_handler.write(rendered_template)

    def generate_template(self, template_name):
        """Creates tf output for every file in our template."""
        try:
            template = self.template_env.get_template(template_name)
            rendered_template = template.render(email=self.default_email)
            LOGGER.info(rendered_template)
            return rendered_template
        except jinja2.exceptions.TemplateNotFound:
            LOGGER.info("No template found for %s", template_name)
            return None
