"""
Show command is used for discovery of detective rules that you may
want to include in your reflex configuration.
"""
import logging

import click

from reflex_cli.rule_discoverer import RuleDiscoverer

LOGGER = logging.getLogger("reflex_cli")


@click.command("show", short_help="Shows possible reflex rules.")
def cli():
    """
    Displays the currently supported common rules provided by reflex.

    Requires access to reflex's internal system manifest at manifest.cloudmitigator.com.
    """
    discoverer = RuleDiscoverer()
    LOGGER.info("Collecting list of available rules...")
    discoverer.collect_rules()
    discoverer.display_discovered_rules()
