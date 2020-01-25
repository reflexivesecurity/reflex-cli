import subprocess
import click
from reflex_cli.cli import pass_environment


@click.command("tf", short_help="`terraform ...`")
@click.argument("tf_args", nargs=-1)
@pass_environment
def cli(ctx, tf_args):
    """
    Wrapper for terraform

    Use `--` to pass additional arguments to terrafrom.

    Example:
        `reflex tf version`
        `reflex tf -- plan -out tf.out`

    """

    tf_args_str = " ".join(tf_args)
    process = subprocess.Popen(f"terraform {tf_args_str}", shell=True)
    stdout, stderr = process.communicate()
