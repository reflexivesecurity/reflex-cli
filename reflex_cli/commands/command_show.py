"""
Show command is used for discovery of detective measures that you may
want to include in your reflex configuration.
"""
import logging

import click

from reflex_cli.measure_discoverer import MeasureDiscoverer

LOGGER = logging.getLogger("reflex_cli")


@click.command("show", short_help="Shows possible reflex measures.")
def cli():
    """CLI entrypoint for show command."""
    discoverer = MeasureDiscoverer()
    LOGGER.info("Collecting list of available measures...")
    discoverer.collect_measures()
    discoverer.display_discovered_measures()
