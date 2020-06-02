"""Command that will create a bootstrapped directory for reflex."""
import logging
import os

import click

from reflex_cli.reflex_initializer import ReflexInitializer

LOGGER = logging.getLogger("reflex_cli")
CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
BOLD = "\033[1m"
ENDC = "\033[0m"


@click.command(
    "init", short_help="Initializes a directory with a configuration file."
)
@click.option(
    "-i",
    "--interactive",
    "interactive",
    is_flag=True,
    default=False,
    help="Prompt user for decision on which individual rules to add to configuration file.",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=False, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
def cli(interactive, config):
    """
    Generates a reflex configuration yaml file to be later used to build reflex infrastructure.

    Default configuration file name is reflex.yaml
    """
    LOGGER.debug("Initializing reflex directory in: %s", config)
    LOGGER.info(
        "%s📝 Generating reflex.yaml config file in: %s%s", BOLD, config, ENDC
    )
    initializer = ReflexInitializer(interactive, config)
    initializer.determine_config_values()
    initializer.write_config_file()
