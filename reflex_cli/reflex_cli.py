"""Entrypoint class for accumulating subcommands by project structure."""
# pylint: disable=arguments-differ
# pylint: disable=unused-argument,inconsistent-return-statements
import logging
import os
import sys
import click

CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class ReflexCli(click.MultiCommand):
    """Class that handles subcommand setup."""

    @staticmethod
    def is_command_file(filename):
        """Determines based on file name if command file."""
        if filename.endswith(".py") and filename.startswith("command_"):
            return True
        return False

    def list_commands(self, context):
        command_files = []
        for filename in os.listdir(CMD_FOLDER):
            if self.is_command_file(filename):
                command_files.append(
                    filename[8:-3]
                )  # Remove "command_" prefix and ".py" suffix
        command_files.sort()
        return command_files

    def get_command(self, context, name):
        try:

            mod = __import__(f"reflex_cli.commands.command_{name}", None, None, ["cli"])
        except ImportError:
            logging.error("%s is not a command for reflex.", name)
            sys.exit(77)
        return mod.cli
