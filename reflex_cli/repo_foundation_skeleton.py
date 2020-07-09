""" Creates templates for new Reflex rules """
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from reflex_cli.create_template_utils import (
    ensure_output_directory_exists,
    write_template_file,
)

LOGGER = logging.getLogger(__name__)
DEFAULT_GITHUB_ORG = "cloudmitigator"


class RepoFoundationSkeleton:
    """Generate a set of templates from a given config."""

    def __init__(
        self, output_directory, configuration
    ):  # pylint: disable=too-many-arguments
        self.output_directory = output_directory
        self.github_org_name = configuration.get("github_org")
        self.rule_name = configuration.get("rule_name")
        self.class_name = configuration.get("class_name")
        self.mode = configuration.get("mode")
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates/rule_templates"),
            autoescape=select_autoescape(["tf"]),
        )

    def create_templates(self):  # pragma: no cover
        """ Generates templates for rule. """
        ensure_output_directory_exists(self.output_directory)
        self.create_workflow_template()
        self.create_source_template()
        self.create_requirements_template()
        self.create_gitignore_template()
        self.create_license_template()
        self.create_readme_template()

    def create_template(
        self, template_file, template_options, output_path
    ):  # pragma: no cover
        """Helper method to create file from rendered jinja."""
        template = self.template_env.get_template(template_file)
        rendered_template = template.render(template_options)
        output_file = os.path.join(self.output_directory, output_path)
        write_template_file(output_file, rendered_template)

    def create_workflow_template(self):  # pragma: no cover
        """ Generates template for GitHub release file """
        self.create_template(
            template_file=".github/workflows/release.yaml.jinja2",
            template_options={},
            output_path=".github/workflows/release.yaml",
        )

    def create_source_template(self):  # pragma: no cover
        """ Generates template for rule source code """
        self.create_template(
            template_file="source/rule.py.jinja2",
            template_options={"rule_class_name": self.class_name, "mode": self.mode,},
            output_path=f"source/{self.rule_name.replace('-', '_')}.py",
        )

    def create_requirements_template(self):  # pragma: no cover
        """ Generates template for requirements.txt """
        require_file = "source/requirements.txt"
        self.create_template(
            template_file=require_file, template_options={}, output_path=require_file,
        )

    def create_gitignore_template(self):  # pragma: no cover
        """ Generates template for .gitignore """
        self.create_template(
            template_file=".gitignore", template_options={}, output_path=".gitignore",
        )

    def create_license_template(self):  # pragma: no cover
        """ Generates template for LICENSE """
        self.create_template(
            template_file="LICENSE", template_options={}, output_path="LICENSE"
        )

    def create_readme_template(self):  # pragma: no cover
        """ Generates template for README.md """
        self.create_template(
            template_file="README.md",
            template_options={
                "github_org_name": self.github_org_name,
                "rule_name": self.rule_name,
            },
            output_path="README.md",
        )
