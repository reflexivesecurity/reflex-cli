"""Holder of template generation logic"""
import os
import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path


class TemplateGenerator:
    """Generate a set of templates from a given config."""
    def __init__(self, configuration, output_directory):
        self.configuration = configuration
        self.output_directory = output_directory
        self.template_env = Environment(
            loader=PackageLoader('reflex_cli', 'templates'),
            autoescape=select_autoescape(['tf'])
        )
        self._ensure_output_directory_exists()

    def _ensure_output_directory_exists(self):
        """Ensure that the path to the output directory exists."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)

    def create_templates(self):
        """Generates templates for every measure in configuration."""
        for measure in self.configuration['measures']:
            default_email = self.configuration['default_notification_email']
            self.generate_template(measure, default_email)

    def generate_template(self, measure, email):
        """Creates tf output for every file in our template."""
        if isinstance(measure, str):
            template_name = measure + '.tf'
        elif isinstance(measure, dict):
            template_name = list(measure)[0] + '.tf'
        try:
            template = self.template_env.get_template(template_name)

            rendered_template = template.render(email=email)
            print(rendered_template)
            output_file = os.path.join(self.output_directory, template_name)
            with open(output_file, 'w+') as file_handler:
                file_handler.write(rendered_template)

        except jinja2.exceptions.TemplateNotFound:
            print(f'No template found for {template_name}')
