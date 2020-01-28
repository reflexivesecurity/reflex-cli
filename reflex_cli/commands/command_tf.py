"""Command to run raw tf commands."""
import logging
import subprocess
import click

LOGGER = logging.getLogger("reflex_cli")


@click.command("tf", short_help="Alias to `terraform`.")
@click.argument("tf_args", nargs=-1)
def cli(tf_args):
    """
    Wrapper for terraform

    Use `--` to pass additional arguments to terrafrom.

    Example:
        `reflex tf version`
        `reflex tf -- plan -out tf.out`

    """

    tf_arguments = " ".join(tf_args)
    LOGGER.debug("tf called with arguments: %s", tf_arguments)
    LOGGER.debug('Executing: "terraform %s"', tf_arguments)
    process = subprocess.Popen(f"terraform {tf_arguments}", shell=True)
    process.wait()
