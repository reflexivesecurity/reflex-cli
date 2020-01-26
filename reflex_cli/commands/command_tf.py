"""Command to run raw tf commands."""
import subprocess
import click


@click.command("tf", short_help="`terraform ...`")
@click.argument("tf_args", nargs=-1)
def cli(tf_args):
    """
    Wrapper for terraform

    Use `--` to pass additional arguments to terrafrom.

    Example:
        `reflex tf version`
        `reflex tf -- plan -out tf.out`

    """

    tf_args_str = " ".join(tf_args)
    subprocess.Popen(f"terraform {tf_args_str}", shell=True)
