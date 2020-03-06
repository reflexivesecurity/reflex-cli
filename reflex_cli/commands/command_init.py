"""Command that will create a bootstrapped directory for reflex."""
import logging
import os

import click

from reflex_cli.reflex_initializer import ReflexInitializer

LOGGER = logging.getLogger("reflex_cli")
CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))


@click.command(
    "init", short_help="Initializes a directory with a configuration file."
)
@click.option(
    "-a",
    "--all",
    "select_all",
    is_flag=True,
    help="Chooses to add all possible rules to configuration.",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=False, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
def cli(select_all, config):
    """Creates a new reflex ready directory structure."""
    LOGGER.debug("Initializing reflex directory in: %s", config)
    LOGGER.info("Generating reflex.yaml config file in: %s", config)
    initializer = ReflexInitializer(select_all, config)
    initializer.determine_config_values()
    initializer.write_config_file()
