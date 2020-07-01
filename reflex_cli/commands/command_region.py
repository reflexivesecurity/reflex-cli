"""
Region command takes in configuration file outputs region
forwarder infrastructure template
"""
# pylint: disable=line-too-long
import logging
import os

import click

from reflex_cli.config_parser import ConfigParser
from reflex_cli.region_template_generator import RegionTemplateGenerator

CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
OUTPUT_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_region"))
LOGGER = logging.getLogger("reflex_cli")
BOLD = "\033[1m"
ENDC = "\033[0m"


@click.command(
    "region", short_help="Builds out tf files for region forwarder architecture.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    default=OUTPUT_DEFAULT,
    help="Output directory for reflex",
)
@click.option(
    "-r",
    "--region",
    help="Region to deploy central forwarding infrastructure.",
    required=True,
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
def cli(output, region, config):
    """
    Builds terraform output for multi-region support of reflex in AWS.

    Region will look at your configuration, generate the relevant templates
    and providers for deploying region forwarders.
    """
    LOGGER.debug("Config file set to: %s", config)
    configuration = ConfigParser(config)
    configuration.parse_valid_config()
    if output == OUTPUT_DEFAULT:
        output = OUTPUT_DEFAULT + "_" + region.replace("-", "_")
    generator = RegionTemplateGenerator(configuration.raw_configuration, output, region)
    LOGGER.info(
        "✍  %s Writing regional terraform files for %s ... %s", BOLD, region, ENDC,
    )
    generator.create_templates()
