"""Command that will create a bootstrapped directory for reflex."""
import logging

import click

from reflex_cli.cli import pass_environment
from reflex_cli.reflex_initializer import ReflexInitializer

LOGGER = logging.getLogger("reflex_cli")


@click.command(
    "init", short_help="Initializes a directory with a configuration file."
)
@pass_environment
def cli(context):
    """Creates a new reflex ready directory structure."""
    LOGGER.debug("Initializing reflex directory in: %s", context.home)
    LOGGER.info("Generating reflex.yaml config file in: %s", context.home)
    initializer = ReflexInitializer(context.home)
    initializer.determine_config_values()
    initializer.write_config_file()
