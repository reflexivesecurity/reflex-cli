"""Build command takes in configuration file outputs infrastructure template"""
# pylint: disable=line-too-long
import logging
import os

import click

from reflex_cli.config_parser import ConfigParser
from reflex_cli.template_generator import TemplateGenerator

CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
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
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
def cli(output, config):
    """
    Builds terraform output files for reflex infrastructure based upon input configuration file.

    By default, build looks for configuration in a local reflex.yaml and outputs built infrastructure to a reflex_out directory.
    """
    LOGGER.debug("Config file set to: %s", config)
    LOGGER.debug("Output directory set to: %s", output)
    configuration = ConfigParser(config)
    configuration.parse_valid_config()
    generator = TemplateGenerator(configuration.raw_configuration, output)
    LOGGER.info("Creating Terraform files...")
    generator.create_templates()
