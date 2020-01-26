"""Command that will create a bootstrapped directory for reflex."""
import click
from reflex_cli.cli import pass_environment
from reflex_cli.reflex_initializer import ReflexInitializer


@click.command("init", short_help="Runs `terraform init`")
@pass_environment
def cli(context):
    """Creates a new reflex ready directory structure."""
    initializer = ReflexInitializer(context.home)
    initializer.determine_config_values()
    initializer.write_config_file()
