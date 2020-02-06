"""
Upgrade command evaluates a current set of templates and
checks whether or not the deployed version could be updated.
"""
import logging

import click

from reflex_cli.cli import pass_environment

LOGGER = logging.getLogger("reflex_cli")

SHORT_UPGRADE_HELP = (
    "Evaluates existing reflex deployment for possible upgrades."
)


@click.command("upgrade", short_help=SHORT_UPGRADE_HELP)
@pass_environment
def cli(context):
    """CLI entrypoint for upgrade command."""
    LOGGER.info(
        "Determining if upgrade is needed for reflex deploy at in: %s",
        context.home,
    )
