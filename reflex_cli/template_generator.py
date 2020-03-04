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
        """Generates templates for every rule in configuration."""
        self.create_notification_template()
        self.create_reflex_kms_template()
        self.create_provider_templates()
        self.create_backend_template()
        for rule in self.configuration["rules"]:
            template_name = self.determine_template_name(rule)
            LOGGER.debug("Rendering template with name: %s", template_name)
            rendered_template = self.generate_template(template_name, rule)
            if rendered_template:
                self.write_template_file(rule, rendered_template)

    def create_notification_template(self):  # pragma: no cover
        """Generates template for central sns topic infrastructure."""
        template = self.template_env.get_template("central-sns-topic.tf")
        rendered_template = template.render(email=self.default_email)
        self.write_template_file(["central-sns-topic"], rendered_template)

    def create_reflex_kms_template(self):  # pragma: no cover
        """Generates template for central sns topic infrastructure."""
        template = self.template_env.get_template("reflex-kms-key.tf")
        rendered_template = template.render()
        self.write_template_file(["reflex-kms-key"], rendered_template)

    def create_provider_templates(self):  # pragma: no cover
        """Creates a simpler provider output file in terraform."""
        for provider in self.configuration["providers"]:
            template = self.template_env.get_template("provider.tf")
            rendered_template = template.render(
                provider_name=list(provider)[0],
                region_name=provider[list(provider)[0]]["region"],
            )
            self.write_template_file(["providers"], rendered_template)

    def create_backend_template(self):  # pragma: no cover
        """Creates a simpler provider output file in terraform."""
        if self.configuration["backend"]:
            template = self.template_env.get_template("backend.tf")
            backend_type = list(self.configuration["backend"])[0]
            rendered_template = template.render(
                backend_type=backend_type,
                backend_config_array=self.configuration["backend"][
                    backend_type
                ],
            )
            self.write_template_file(["backend"], rendered_template)

    @staticmethod
    def determine_template_name(rule):
        """Inspects instance type of rule to determine file name."""
        if isinstance(rule, str):
            template_name = rule + ".tf"
        elif isinstance(rule, dict):
            template_name = list(rule)[0] + ".tf"

        if "aws-detect" in template_name:
            return "aws-detect.tf"
        if "aws-enforce" in template_name:
            return "aws-enforce.tf"
        return None

    def generate_template(self, template_name, rule):  # pragma: no cover
        """Creates tf output for every file in our template."""
        template = self.template_env.get_template(template_name)
        rule_name = list(rule)[0]

        if "github_org" in rule[rule_name]:
            github_org = rule[rule_name]["github_org"]
        else:
            github_org = DEFAULT_GITHUB_ORG

        rendered_template = template.render(
            module_name=rule_name,
            template_name=rule_name,
            version=rule[rule_name]["version"],
            github_org=github_org,
        )
        LOGGER.debug(rendered_template)
        return rendered_template

    def write_template_file(self, rule, rendered_template):
        """Writes output of rendering to file"""
        self._ensure_output_directory_exists()
        template_name = list(rule)[0] + ".tf"
        output_file = os.path.join(self.output_directory, template_name)
        LOGGER.info("Creating %s", output_file)
        with open(output_file, "w+") as file_handler:
            file_handler.write(rendered_template)

    def _ensure_output_directory_exists(self):
        """Ensure that the path to the output directory exists."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
