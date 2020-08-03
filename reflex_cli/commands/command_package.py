"""Package command takes in configuration file and generates lambda packages for
each Rule.
"""
import logging
import os

import click

# from PyInquirer import prompt
from reflex_cli.config_parser import ConfigParser

# from reflex_cli.region_template_generator import RegionTemplateGenerator
# from reflex_cli.template_generator import TemplateGenerator
from reflex_cli.package_generator import PackageGenerator

# REGION_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_region"))
CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
OUTPUT_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "package_build"))
LOGGER = logging.getLogger(__name__)
# PLACEHOLDER_EMAIL = "placeholder@example.com"
# BOLD = "\033[1m"
# ENDC = "\033[0m"


@click.command("package", short_help="Generate lambda packages from config file.")
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    default=OUTPUT_DEFAULT,
    help="Output directory for packages",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
@click.option(
    "-m",
    "--custom-rule-module",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=None,
    help="Custom AWSRule file location",
)
@click.option(
    "-a",
    "--additional-requirements",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=[],
    help="Path to additional requirements.txt files declaring additional dependencies to include",
    multiple=True,
)
@click.option(
    "-f",
    "--additional-files",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=[],
    help="Additional files to include in your packages",
    multiple=True,
)
def cli(output, config, custom_rule_module, additional_requirements, additional_files):
    """
    Builds lambda deployment packages for reflex rules based on input configuration file.

    By default, package looks for configuration in a local reflex.yaml and outputs
    built packages to a build directory.
    """
    LOGGER.debug("Config file set to: %s", config)
    LOGGER.debug("Output directory set to: %s", output)
    configuration = ConfigParser(config)
    configuration.parse_valid_config()

    package_generator = PackageGenerator(
        output_directory=output,
        custom_rule_path=custom_rule_module,
        additional_requirements=additional_requirements,
        additional_files=additional_files,
    )

    for reflex_rule in configuration.rule_list:
        package_generator.generate_package(reflex_rule)
