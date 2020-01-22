import subprocess
import click
import os
import yaml
import jinja2
from reflex_cli.cli import pass_environment
from jinja2 import Environment, PackageLoader, select_autoescape

config_default = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))

template_env = Environment(
    loader=PackageLoader('reflex_cli', 'templates'),
    autoescape=select_autoescape(['tf'])
)

def validate_config(config):
    pass

def generate_template(measure, email):
    if type(measure) is str:
        template_name = measure + '.tf'
    elif type(measure) is dict:
        template_name = list(measure)[0] + '.tf'
    try:
        template = template_env.get_template(template_name)
        print(template.render(email=email))
        print(template)
    except jinja2.exceptions.TemplateNotFound:
        print(f'No template found for {template_name}')



@click.command("apply", short_help="Runs `terraform apply`")
@click.option("-c", "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=config_default,
    help="Configuration file for reflex")
@pass_environment
def cli(ctx, config):
    with open(config, 'r') as config_file:
        configuration = yaml.safe_load(config_file)
        validate_config(configuration)
    print(configuration)

    for measure in configuration['measures']:
        generate_template(measure, configuration['default_notification_email'])

