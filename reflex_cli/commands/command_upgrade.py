"""
Upgrade command evaluates a current set of templates and
checks whether or not the deployed version could be updated.
"""
# pylint: disable=line-too-long
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
    help="Chooses to upgrade all possible rules.",
)
@click.option(
    "-r",
    "--rule",
    help="Specify a rule that you would like to upgrade."
)
def cli(rule, select_all, config):
    """
    Compares a local configuration file with external version information to allow users to upgrade rule versions automatically within their configuration.

    By default, configuration file name is set to be reflex.yaml.
    """
    LOGGER.info(
        "Determining if upgrade is needed for reflex deploy at in: %s", config
    )
    updater = ConfigVersionUpdater(config, select_all)
    if rule:
        updater.compare_current_rule_version(rule)
    else:
        updater.compare_current_rule_versions()
    updater.overwrite_reflex_config()
