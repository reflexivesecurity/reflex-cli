"""Holder of template generation logic"""
import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape


class TemplateGenerator:
    """Generate a set of templates from a given config."""
    def __init__(self, configuration):
        self.configuration = configuration
        self.template_env = Environment(
            loader=PackageLoader('reflex_cli', 'templates'),
            autoescape=select_autoescape(['tf'])
        )

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
            print(template.render(email=email))
        except jinja2.exceptions.TemplateNotFound:
            print(f'No template found for {template_name}')
