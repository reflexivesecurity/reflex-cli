"""Entrypoint class for accumulating subcommands by project structurei."""
import os
import sys
import click

CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class ReflexCli(click.MultiCommand):
    """Class that handles subcommand setup."""

    def list_commands(self, context):
        command_files = []
        for filename in os.listdir(CMD_FOLDER):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                command_files.append(filename[4:-3])
        command_files.sort()
        return command_files

    def get_command(self, context, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__("reflex_cli.commands.cmd_" + name, None, None, ["cli"])
        except ImportError:
            return
        return mod.cli
