"""Holder of template generation logic"""
import logging
import os
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

LOGGER = logging.getLogger("reflex_cli")
DEFAULT_GITHUB_ORG = "cloudmitigator"
BOLD = "\033[1m"
ENDC = "\033[0m"


class TemplateGenerator:
    """Generate a set of templates from a given config."""

    def __init__(self, configuration, output_directory):
        self.configuration = configuration
        self.output_directory = output_directory
        self.template_env = Environment(
            loader=PackageLoader("reflex_cli", "templates"),
            autoescape=select_autoescape(["tf"]),
        )
        self.default_email = self.configuration["globals"].get("default_email")

    def create_templates(self):  # pragma: no cover
        """Generates templates for every rule in configuration."""
        self.create_notification_template()
        self.create_reflex_kms_template()
        self.create_provider_templates()
        self.create_backend_template()
        self.create_rule_templates()

    def create_notification_template(self):  # pragma: no cover
        """Generates template for central sns topic infrastructure."""
        template = self.template_env.get_template("central-sns-topic.tf")
        rendered_template = template.render(
            email=self.default_email,
            engine_version=self.configuration["engine_version"],
        )
        self.build_output_file(["central-sns-topic"], rendered_template)

    def create_reflex_kms_template(self):  # pragma: no cover
        """Generates template for central sns topic infrastructure."""
        template = self.template_env.get_template("reflex-kms-key.tf")
        rendered_template = template.render(
            engine_version=self.configuration["engine_version"]
        )
        self.build_output_file(["reflex-kms-key"], rendered_template)

    def create_provider_templates(self):  # pragma: no cover
        """Creates a simpler provider output file in terraform."""
        for provider in self.configuration["providers"]:
            template = self.template_env.get_template("provider.tf")
            rendered_template = template.render(
                provider_name=list(provider)[0],
                region_name=provider[list(provider)[0]]["region"],
            )
            self.build_output_file(["providers"], rendered_template)

    def create_backend_template(self):  # pragma: no cover
        """Creates a simpler provider output file in terraform."""
        if self.configuration["backend"]:
            template = self.template_env.get_template("backend.tf")
            backend_type = list(self.configuration["backend"])[0]
            rendered_template = template.render(
                backend_type=backend_type,
                backend_config_array=self.configuration["backend"][backend_type],
            )
            self.build_output_file(["backend"], rendered_template)

    def create_rule_templates(self):
        """Creates tf file for each rule"""
        for rule in self.configuration["rules"]["aws"]:
            rendered_template = self.generate_template("aws-rule.tf", rule)
            if rendered_template:
                self.build_output_file(rule, rendered_template)

    def generate_template(self, template_name, rule):  # pragma: no cover
        """Creates tf output for every file in our template."""
        template = self.template_env.get_template(template_name)
        rule_name = list(rule)[0]

        github_org = rule[rule_name].get("github_org", DEFAULT_GITHUB_ORG)
        if github_org == DEFAULT_GITHUB_ORG:
            repo_name = f"reflex-aws-{rule_name}"
        else:
            repo_name = rule_name

        rendered_template = template.render(
            module_name=rule_name,
            cwe_module_name=f"{rule_name}-cwe",
            template_name=repo_name,
            version=rule[rule_name]["version"],
            github_org=github_org,
            configuration=rule[rule_name].get("configuration"),
        )
        LOGGER.debug(rendered_template)
        return rendered_template

    @staticmethod
    def build_template_names_from_rule(rule):
        """Returns rule name with tf appended."""
        return list(rule)[0] + ".tf"

    def build_output_file(self, rule, rendered_template):
        """Build output file name to write rendering to file"""
        template_name = self.build_template_names_from_rule(rule)
        output_file = os.path.join(self.output_directory, template_name)
        self.write_template_file(output_file, rendered_template)

    def write_template_file(self, output_file, rendered_template):  # pragma: no cover
        """Writes output of rendering to file"""
        self._ensure_output_directory_exists()
        LOGGER.info("📃 Writing terraform file to: %s%s%s", BOLD, output_file, ENDC)
        with open(output_file, "w+") as file_handler:
            file_handler.write(rendered_template)

    def _ensure_output_directory_exists(self):  # pragma: no cover
        """Ensure that the path to the output directory exists."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
