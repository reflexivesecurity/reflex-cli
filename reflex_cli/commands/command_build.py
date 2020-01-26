"""Build command takes in configuration file outputs infrastructure template"""
import os
import click
from reflex_cli.config_parser import ConfigParser
from reflex_cli.template_generator import TemplateGenerator

CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
OUTPUT_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_out"))


@click.command("build", short_help="Builds out tf files from config file.")
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(
        exists=False, dir_okay=True, file_okay=False, resolve_path=True
    ),
    default=OUTPUT_DEFAULT,
    help="Output directory for reflex",
)
def cli(config, output):
    """CLI entrypoint for build command."""
    configuration = ConfigParser(config)
    config_dictionary = configuration.generate_config()
    generator = TemplateGenerator(config_dictionary, output)
    generator.create_templates()
