"""Entrypoint for our reflex CLI application."""
# pylint: disable=invalid-name,no-value-for-parameter
import logging
import os
import sys

import click

from reflex_cli.cli_environment import CliEnvironment
from reflex_cli.reflex_cli import ReflexCli

FORMAT = "%(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.INFO)
LOGGER = logging.getLogger("reflex_cli")

CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
CONTEXT_SETTINGS = {"auto_envvar_prefix": "reflex"}

pass_environment = click.make_pass_decorator(CliEnvironment, ensure=True)


@click.command(cls=ReflexCli, context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    "--home",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the folder to operate on.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(context, verbose, home):
    """
    CLI interface for building infrastructure to deploy the reflex cloud security framework.

    To learn more about reflex, check out https://docs.cloudmitigator.com.

    Get started by building a configuration file with `reflex init`.
    """
    context.verbose = verbose
    if context.verbose:
        LOGGER.setLevel(logging.DEBUG)
    if home is not None:
        context.home = home
    LOGGER.debug("home set to: %s", context.home)


if __name__ == "__main__":
    cli()
