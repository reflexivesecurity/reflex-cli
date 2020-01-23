"""Build command takes in configuration file outputs infrastructure template"""
import os
import click
from reflex_cli.config_parser import ConfigParser
from reflex_cli.template_generator import TemplateGenerator
from reflex_cli.cli import pass_environment

CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))


@click.command("apply", short_help="Runs `terraform apply`")
@click.option("-c",
              "--config",
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              default=CONFIG_DEFAULT,
              help="Configuration file for reflex")
@pass_environment
def cli(ctx, config):
    """CLI entrypoint for build command."""
    configuration = ConfigParser(config)
    config_dictionary = configuration.generate_config()
    generator = TemplateGenerator(config_dictionary)
    generator.create_templates()
