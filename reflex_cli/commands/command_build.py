"""Build command takes in configuration file outputs infrastructure template"""
import logging
import os

import click

from reflex_cli.cli import pass_environment
from reflex_cli.config_parser import ConfigParser
from reflex_cli.template_generator import TemplateGenerator

OUTPUT_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_out"))
LOGGER = logging.getLogger("reflex_cli")


@click.command("build", short_help="Builds out tf files from config file.")
@click.option(
    "-o",
    "--output",
    type=click.Path(
        exists=False, dir_okay=True, file_okay=False, resolve_path=True
    ),
    default=OUTPUT_DEFAULT,
    help="Output directory for reflex",
)
@pass_environment
def cli(context, output):
    """CLI entrypoint for build command."""
    LOGGER.debug("Config file set to: %s", context.config)
    LOGGER.debug("Output directory set to: %s", output)
    configuration = ConfigParser(context.config)
    config_dictionary = configuration.parse_valid_config()
    generator = TemplateGenerator(config_dictionary, output)
    LOGGER.info("Creating Terraform files...")
    generator.create_templates()
