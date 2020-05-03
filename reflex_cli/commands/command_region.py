"""Region command takes in configuration file outputs region forwarder infrastructure template"""
# pylint: disable=line-too-long
import logging
import os

import click

from reflex_cli.config_parser import ConfigParser
from reflex_cli.template_generator import TemplateGenerator

CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
LOGGER = logging.getLogger("reflex_cli")


@click.command(
    "region",
    short_help="Builds out tf files for region forwarder architecture.",
)
@click.option("-r", "--region", help="Region to forward to central region")
@click.option(
    "-q", "--central-sqs-arn", help="SQS Queue arn in central processing region"
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
def cli(region, central_sqs_arn, config):
    """
    Builds terraform output files for the multi-region support of reflex in AWS.

    Region will look at your configuration, generate the relevant templates and providers for deploying region forwarders.
    """
    LOGGER.debug("Config file set to: %s", config)
