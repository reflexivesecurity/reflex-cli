""" Creates templates for new Reflex rules """
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from reflex_cli.create_template_utils import (
    ensure_output_directory_exists,
    write_template_file,
)
from reflex_cli.rule_discoverer import RuleDiscoverer

LOGGER = logging.getLogger(__name__)


class TerraformSkeleton:
    """Generate a set of templates from a given config."""

    def __init__(self, output_directory, configuration):
        self.output_directory = output_directory
        self.rule_name = configuration.get("rule_name")
        self.class_name = configuration.get("class_name")
        self.engine_version = self.get_engine_version()
        self.mode = configuration.get("mode")
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates/rule_templates"),
            autoescape=select_autoescape(["tf"]),
        )

    def create_templates(self):  # pragma: no cover
        """ Generates templates for rule. """
        ensure_output_directory_exists(self.output_directory)
        self.create_cwe_terraform_template()
        self.create_cwe_output_template()
        self.create_sqs_lambda_terraform_template()
        self.create_variables_terraform_template()

    def create_template(
        self, template_file, template_options, output_path
    ):  # pragma: no cover
        """Helper method to create file from rendered jinja."""
        template = self.template_env.get_template(template_file)
        rendered_template = template.render(template_options)
        output_file = os.path.join(self.output_directory, output_path)
        write_template_file(output_file, rendered_template)

    def create_cwe_terraform_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        self.create_template(
            template_file="cwe.tf",
            template_options={
                "rule_class_name": self.class_name,
                "engine_version": self.engine_version,
            },
            output_path="terraform/cwe/cwe.tf",
        )

    def create_cwe_output_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        self.create_template(
            template_file="output.tf",
            template_options={},
            output_path="terraform/cwe/output.tf",
        )

    def create_sqs_lambda_terraform_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        self.create_template(
            template_file="sqs_lambda.tf",
            template_options={
                "rule_name": self.rule_name,
                "rule_class_name": self.class_name,
                "mode": self.mode,
                "engine_version": self.engine_version,
            },
            output_path="terraform/sqs_lambda/sqs_lambda.tf",
        )

    def create_variables_terraform_template(self):  # pragma: no cover
        """Creates tf output for every file in our template."""
        self.create_template(
            template_file="variables.tf",
            template_options={"mode": self.mode},
            output_path="terraform/sqs_lambda/variables.tf",
        )

    @staticmethod
    def get_engine_version():
        """ Pulls current engine version from manifest."""
        measure_manifest = RuleDiscoverer()
        engine_dictionary = measure_manifest.collect_engine()
        return engine_dictionary["reflex-engine"]["version"]
