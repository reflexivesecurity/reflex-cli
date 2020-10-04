"""Build command takes in configuration file outputs infrastructure template"""
# pylint: disable=line-too-long
import logging
import os
import sys

import click

from PyInquirer import prompt
from reflex_cli.config_parser import ConfigParser
from reflex_cli.region_template_generator import RegionTemplateGenerator
from reflex_cli.child_template_generator import ChildTemplateGenerator
from reflex_cli.template_generator import TemplateGenerator

REGION_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_region"))
CHILD_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_child"))
CONFIG_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex.yaml"))
OUTPUT_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "reflex_out"))
PACKAGE_DEFAULT = os.path.abspath(os.path.join(os.getcwd(), "package_build"))
LOGGER = logging.getLogger("reflex_cli")
PLACEHOLDER_EMAIL = "placeholder@example.com"
BOLD = "\033[1m"
ENDC = "\033[0m"


@click.command("build", short_help="Builds out tf files from config file.")
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    default=OUTPUT_DEFAULT,
    help="Output directory for reflex",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=CONFIG_DEFAULT,
    help="Configuration file for reflex",
)
def cli(output, config):
    """
    Builds terraform output files for reflex infrastructure based upon input configuration file.

    By default, build looks for configuration in a local reflex.yaml and outputs built infrastructure to a reflex_out directory.
    """
    LOGGER.debug("Config file set to: %s", config)
    LOGGER.debug("Output directory set to: %s", output)
    configuration = ConfigParser(config)
    configuration.parse_valid_config()
    if not os.path.exists(PACKAGE_DEFAULT):
        LOGGER.info("✍  %s Package directory nonexistent, creating ...%s", BOLD, ENDC)
        os.system("reflex package")
    if configuration.raw_configuration["globals"]["default_email"] == PLACEHOLDER_EMAIL:
        questions = [
            {
                "type": "confirm",
                "message": "Notification email is left as placeholder. Edit before build?",
                "name": "edit_email",
                "default": True,
            }
        ]
        answers = prompt(questions)
        # TODO: When a new release of PyInquirer comes out, we should use their
        #       new feature to raise the keyboard interrupt instead of catching
        #       the KeyError.  prompt(questions, raise_keyboard_interrupt=True)
        try:
            if answers["edit_email"]:
                email_form = [
                    {
                        "type": "input",
                        "name": "default_email",
                        "message": "Default email address for reflex notifications:",
                    }
                ]
                email = prompt(email_form)["default_email"]
                configuration.raw_configuration["globals"]["default_email"] = email
        except KeyError:
            sys.exit(1)
    generator = TemplateGenerator(configuration.raw_configuration, output)
    LOGGER.info("✍  %s Writing terraform output files ...%s", BOLD, ENDC)
    generator.create_templates()
    aws_provider = configuration.raw_configuration["providers"][0]["aws"]
    if aws_provider.get("forwarding_regions"):
        for region in aws_provider.get("forwarding_regions"):
            output_file = REGION_DEFAULT + "_" + region.replace("-", "_")
            generator = RegionTemplateGenerator(
                configuration.raw_configuration, output_file, region
            )
            LOGGER.info("✍  %s Writing terraform output files ...%s", BOLD, ENDC)
            generator.create_templates()
    if aws_provider.get("child_accounts"):
        parent_account_id = aws_provider.get("parent_account")
        if not parent_account_id:
            parent_account_form = [
                {
                    "type": "input",
                    "name": "parent_account",
                    "message": "Parent reflex AWS account ID for multi-account support:",
                }
            ]
            parent_account_id = prompt(parent_account_form)["default_email"]
        for child_account in aws_provider.get("child_accounts"):
            output_file = CHILD_DEFAULT + "_" + str(child_account)
            generator = ChildTemplateGenerator(
                configuration.raw_configuration,
                output_file,
                str(child_account),
                str(parent_account_id),
            )
            LOGGER.info("✍  %s Writing terraform output files ...%s", BOLD, ENDC)
            generator.create_templates()
