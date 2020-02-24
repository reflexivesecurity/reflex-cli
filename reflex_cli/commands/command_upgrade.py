"""
Upgrade command evaluates a current set of templates and
checks whether or not the deployed version could be updated.
"""
import logging
import os

import click

from reflex_cli.config_version_updater import ConfigVersionUpdater

LOGGER = logging.getLogger("reflex_cli")
CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))

SHORT_UPGRADE_HELP = (
    "Evaluates existing reflex deployment for possible upgrades."
)


@click.command("upgrade", short_help=SHORT_UPGRADE_HELP)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex.",
)
@click.option(
    "-a",
    "--all",
    "select_all",
    is_flag=True,
    help="Chooses to upgrade all possible measures.",
)
def cli(select_all, config):
    """CLI entrypoint for upgrade command."""
    LOGGER.info(
        "Determining if upgrade is needed for reflex deploy at in: %s", config
    )
    updater = ConfigVersionUpdater(config, select_all)
    updater.compare_current_rule_versions()
    updater.overwrite_reflex_config()
