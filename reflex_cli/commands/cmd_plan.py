import subprocess
import click
from reflex_cli.cli import pass_environment


@click.command("plan", short_help="Runs `terraform plan`")
@click.argument("tf_args", nargs=-1)
@pass_environment
def cli(ctx):
    """
    Run apply, which runs terraform apply

    Generates an execution plan for Terraform.

    This execution plan can be reviewed prior to running apply to get a
    sense for what Terraform will do. Optionally, the plan can be saved to
    a Terraform plan file, and apply can take this plan file to execute
    this plan exactly.
    """

    tf_args_str = " ".join(tf_args)
    process = subprocess.Popen("terraform plan {tf_args_str}", shell=True)
    stdout, stderr = process.communicate()

    ctx.log(stdout)
    ctx.log(stderr)
