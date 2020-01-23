"""Class to create decorator for command classes."""
import os
import sys
import click


class CliEnvironment:
    """Helper class for click specific commands."""

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    @staticmethod
    def log(msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)
