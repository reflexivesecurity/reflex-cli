"""
Create is used to generate a skeleton for a new Reflex rule
"""
import logging
import os

import click

from reflex_cli.rule_template_generator import RuleTemplateGenerator

LOGGER = logging.getLogger(__name__)
DEFAULT_GITHUB_ORG = "cloudmitigator"
BOLD = "\033[1m"
ENDC = "\033[0m"


@click.command("create", short_help="Create a new reflex rule.")
@click.option(
    "-o",
    "--output",
    type=click.Path(
        exists=False, dir_okay=True, file_okay=False, resolve_path=True
    ),
    help="Output directory for this reflex rule",
)
@click.option(
    "-r",
    "--rule-name",
    type=str,
    help="The kebab-case name for your rule. Example: my-encryption-rule",
    prompt="The kebab-case name for your rule.",
)
@click.option(
    "-c",
    "--class-name",
    type=str,
    help="The PascalCase name for your rule. Example: MyEncryptionRule",
    prompt="The PascalCase name for your rule.",
)
@click.option(
    "-m",
    "--mode",
    type=str,
    help="The mode for your rule. Options: DETECT | REMEDIATE",
    prompt="The mode for your rule. [DETECT | REMEDIATE]",
)
def cli(output, rule_name, class_name, mode):
    """
    Creates a skeleton rule directory to enable the faster creation of custom reflex rules.

    For further information on creating rules for reflex, check out https://docs.cloudmitigator.com.
    """
    if output:
        output_directory = os.path.abspath(os.path.join(os.getcwd(), output))
    else:
        output_directory = os.path.abspath(os.path.join(os.getcwd(), rule_name))
    github_org_name = DEFAULT_GITHUB_ORG

    template_generator = RuleTemplateGenerator(
        output_directory=output_directory,
        github_org_name=github_org_name,
        rule_name=rule_name,
        class_name=class_name,
        mode=mode,
    )
    LOGGER.info("%s🎨 Generating custom rule template files...%s", BOLD, ENDC)
    template_generator.create_templates()
