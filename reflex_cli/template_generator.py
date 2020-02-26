"""Holder of template generation logic"""
import logging
import os
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

LOGGER = logging.getLogger("reflex_cli")
DEFAULT_GITHUB_ORG = "cloudmitigator"

class TemplateGenerator:
    """Generate a set of templates from a given config."""

    def __init__(self, configuration, output_directory):
        self.configuration = configuration
        self.output_directory = output_directory
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates"),
            autoescape=select_autoescape(["tf"]),
        )
        self.default_email = self.configuration.get("default_email")

    def create_templates(self):  # pragma: no cover
        """Generates templates for every measure in configuration."""
        self.create_provider_templates()
        for measure in self.configuration["measures"]:
            template_name = self.determine_template_name(measure)
            LOGGER.debug("Rendering template with name: %s", template_name)
            rendered_template = self.generate_template(template_name, measure)
            if rendered_template:
                self.write_template_file(measure, rendered_template)

    def create_provider_templates(self):  # pragma: no cover
        """Creates a simpler provider output file in terraform."""
        for provider in self.configuration["providers"]:
            template = self.template_env.get_template("provider.tf")
            rendered_template = template.render(
                provider_name=list(provider)[0],
                region_name=provider[list(provider)[0]]["region"],
            )
            self.write_template_file(["providers"], rendered_template)

    @staticmethod
    def determine_template_name(measure):
        """Inspects instance type of measure to determine file name."""
        if isinstance(measure, str):
            template_name = measure + ".tf"
        elif isinstance(measure, dict):
            template_name = list(measure)[0] + ".tf"

        if "aws-detect" in template_name:
            return "aws-detect.tf"
        if "aws-enforce" in template_name:
            return "aws-enforce.tf"
        return None

    def generate_template(self, template_name, measure):  # pragma: no cover
        """Creates tf output for every file in our template."""
        template = self.template_env.get_template(template_name)
        measure_name = list(measure)[0]

        if "github_org" in measure[measure_name]:
            github_org = measure[measure_name]["github_org"]
        else:
            github_org = DEFAULT_GITHUB_ORG

        rendered_template = template.render(
            module_name=measure_name,
            template_name=measure_name,
            email=self.default_email,
            version=measure[measure_name]["version"],
            github_org=github_org
        )
        LOGGER.debug(rendered_template)
        return rendered_template

    def write_template_file(self, measure, rendered_template):
        """Writes output of rendering to file"""
        self._ensure_output_directory_exists()
        template_name = list(measure)[0] + ".tf"
        output_file = os.path.join(self.output_directory, template_name)
        LOGGER.info("Creating %s", output_file)
        with open(output_file, "w+") as file_handler:
            file_handler.write(rendered_template)

    def _ensure_output_directory_exists(self):
        """Ensure that the path to the output directory exists."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
