""" Creates templates for new Reflex rules """
import logging
import os
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from reflex_cli.rule_discoverer import RuleDiscoverer

LOGGER = logging.getLogger(__name__)
DEFAULT_GITHUB_ORG = "cloudmitigator"


class RuleTemplateGenerator:
    """Generate a set of templates from a given config."""

    def __init__(
        self, output_directory, github_org_name, rule_name, class_name, mode
    ):  # pylint: disable=too-many-arguments
        self.output_directory = output_directory
        self.github_org_name = github_org_name
        self.rule_name = rule_name
        self.class_name = class_name
        self.engine_version = self.get_engine_version()
        self.mode = mode
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates/rule_templates"),
            autoescape=select_autoescape(["tf"]),
        )

    def create_templates(self):  # pragma: no cover
        """ Generates templates for rule. """
        self.create_workflow_template()
        self.create_source_template()
        self.create_requirements_template()
        self.create_gitignore_template()
        self.create_license_template()
        self.create_readme_template()
        self.create_cwe_terraform_template()
        self.create_cwe_output_template()
        self.create_sqs_lambda_terraform_template()
        self.create_variables_terraform_template()

    def create_template(self, template_file, template_options, output_path):
        """Helper method to create file from rendered jinja."""
        template = self.template_env.get_template(template_file)
        rendered_template = template.render(template_options)
        output_file = os.path.join(self.output_directory, output_path)
        self.write_template_file(output_file, rendered_template)

    def create_workflow_template(self):  # pragma: no cover
        """ Generates template for GitHub release file """
        self.create_template(
            ".github/workflows/release.yaml.jinja2",
            None,
            ".github/workflows/release.yaml",
        )

    def create_source_template(self):  # pragma: no cover
        """ Generates template for rule source code """
        self.create_template(
            "source/rule.py.jinja2",
            {"rule_cliass_name": self.class_name, "mode": self.mode},
            f"source/{self.rule_name.replace('-', '_')}.py",
        )

    def create_requirements_template(self):  # pragma: no cover
        """ Generates template for requirements.txt """
        self.create_template(
            "source/requirements.txt", None, "source/requirements.txt"
        )

    def create_gitignore_template(self):  # pragma: no cover
        """ Generates template for .gitignore """
        self.create_template(".gitignore", None, ".gitignore")

    def create_license_template(self):  # pragma: no cover
        """ Generates template for LICENSE """
        self.create_template("LICENSE", None, "LICENSE")

    def create_readme_template(self):  # pragma: no cover
        """ Generates template for README.md """
        self.create_template(
            "README.md",
            {
                "github_org_name": self.github_org_name,
                "rule_name": self.rule_name,
            },
            "README.md",
        )

    def create_cwe_terraform_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        self.create_template(
            "cwe.tf",
            {
                "rule_class_name": self.class_name,
                "engine_version": self.engine_version,
            },
            "terraform/cwe/cwe.tf",
        )

    def create_cwe_output_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        self.create_template("output.tf", None, "terraform/cwe/output.tf")

    def create_sqs_lambda_terraform_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        self.create_template(
            "sqs_lambda.tf",
            {
                "rule_name": self.rule_name,
                "rule_class_name": self.class_name,
                "mode": self.mode,
                "engine_version": self.engine_version,
            },
            "terraform/sqs_lambda/sqs_lambda.tf",
        )

    def create_variables_terraform_template(self):  # pragma: no cover
        """Creates tf output for every file in our template."""
        self.create_template(
            "variables.tf",
            {"mode": self.mode},
            "terraform/sqs_lambda/variables.tf",
        )

    def write_template_file(
        self, output_file, rendered_template
    ):  # pragma: no cover
        """Writes output of rendering to file"""
        self._ensure_output_directory_exists()
        LOGGER.info("Creating %s", output_file)
        with open(output_file, "w+") as file_handler:
            file_handler.write(rendered_template)

    @staticmethod
    def get_engine_version():
        """ Pulls current engine version from manifest."""
        measure_manifest = RuleDiscoverer()
        engine_dictionary = measure_manifest.collect_engine()
        return engine_dictionary["reflex-engine"]["version"]

    def _ensure_output_directory_exists(self):  # pragma: no cover
        """Ensure that the path to the output directory exists."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        Path(self.output_directory + "/source").mkdir(
            parents=True, exist_ok=True
        )
        Path(self.output_directory + "/.github/workflows").mkdir(
            parents=True, exist_ok=True
        )
        Path(self.output_directory + "/terraform/cwe").mkdir(
            parents=True, exist_ok=True
        )
        Path(self.output_directory + "/terraform/sqs_lambda").mkdir(
            parents=True, exist_ok=True
        )
