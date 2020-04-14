""" Creates templates for new Reflex rules """
import logging
import os
import sys
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
        self.mode = mode
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates/rule_templates"),
            autoescape=select_autoescape(["tf"]),
        )

    def create_templates(self):  # pragma: no cover
        """ Generates templates for rule. """
        self.create_directories()
        self.create_workflow_template()
        self.create_source_template()
        self.create_requirements_template()
        self.create_gitignore_template()
        self.create_license_template()
        self.create_readme_template()
        self.create_rule_terraform_template()
        self.create_variables_terraform_template()

    def create_directories(self):  # pragma: no cover
        """ Creates required directories for outputting templates """
        try:
            os.makedirs(
                os.path.join(self.output_directory, ".github/workflows/")
            )
            os.makedirs(os.path.join(self.output_directory, "source"))
        except FileExistsError:
            LOGGER.error(
                "The specified output directory already exists. Delete it or "
                "select a different name and try again."
            )
            sys.exit(1)

    def create_workflow_template(self):  # pragma: no cover
        """ Generates template for GitHub release file """
        template = self.template_env.get_template(
            ".github/workflows/release.yaml.jinja2"
        )
        rendered_template = template.render()
        output_file = os.path.join(
            self.output_directory, ".github/workflows/release.yaml"
        )
        self.write_template_file(output_file, rendered_template)

    def create_source_template(self):  # pragma: no cover
        """ Generates template for rule source code """
        template = self.template_env.get_template("source/rule.py.jinja2")
        rendered_template = template.render(
            rule_class_name=self.class_name, mode=self.mode
        )
        output_file = os.path.join(
            self.output_directory,
            f"source/{self.rule_name.replace('-', '_')}.py",
        )
        self.write_template_file(output_file, rendered_template)

    def create_requirements_template(self):  # pragma: no cover
        """ Generates template for requirements.txt """
        template = self.template_env.get_template("source/requirements.txt")
        rendered_template = template.render()
        output_file = os.path.join(
            self.output_directory, "source/requirements.txt"
        )
        self.write_template_file(output_file, rendered_template)

    def create_gitignore_template(self):  # pragma: no cover
        """ Generates template for .gitignore """
        template = self.template_env.get_template(".gitignore")
        rendered_template = template.render()
        output_file = os.path.join(self.output_directory, ".gitignore")
        self.write_template_file(output_file, rendered_template)

    def create_license_template(self):  # pragma: no cover
        """ Generates template for LICENSE """
        template = self.template_env.get_template("LICENSE")
        rendered_template = template.render()
        output_file = os.path.join(self.output_directory, "LICENSE")
        self.write_template_file(output_file, rendered_template)

    def create_readme_template(self):  # pragma: no cover
        """ Generates template for README.md """
        template = self.template_env.get_template("README.md")
        rendered_template = template.render(
            github_org_name=self.github_org_name, rule_name=self.rule_name
        )
        output_file = os.path.join(self.output_directory, "README.md")
        self.write_template_file(output_file, rendered_template)

    def create_rule_terraform_template(self):  # pragma: no cover
        """ Generates a .tf module for our rule """
        engine_version = self.get_engine_version()
        template = self.template_env.get_template("rule_module.tf")
        rendered_template = template.render(
            rule_name=self.rule_name,
            rule_class_name=self.class_name,
            mode=self.mode,
            engine_version=engine_version,
        )
        output_file = os.path.join(
            self.output_directory, f"{self.rule_name.replace('-', '_')}.tf"
        )
        self.write_template_file(output_file, rendered_template)

    def create_variables_terraform_template(self):  # pragma: no cover
        """Creates tf output for every file in our template."""
        template = self.template_env.get_template("variables.tf")
        rendered_template = template.render(mode=self.mode)
        output_file = os.path.join(self.output_directory, "variables.tf")
        self.write_template_file(output_file, rendered_template)

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
