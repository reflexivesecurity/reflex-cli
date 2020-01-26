"""Entrypoint for our reflex CLI application."""
# pylint: disable=invalid-name,no-value-for-parameter
import click
from reflex_cli.cli_environment import CliEnvironment
from reflex_cli.reflex_cli import ReflexCli


CONTEXT_SETTINGS = dict(auto_envvar_prefix="reflex")

pass_environment = click.make_pass_decorator(CliEnvironment, ensure=True)


@click.command(cls=ReflexCli, context_settings=CONTEXT_SETTINGS)
@click.option(
    "--home",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the folder to operate on.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(context, verbose, home):
    """A reflex command line interface."""
    context.verbose = verbose
    if home is not None:
        context.home = home


if __name__ == "__main__":
    cli()
