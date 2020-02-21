"""Class to create decorator for command classes."""
# pylint: disable=too-few-public-methods
import os


class CliEnvironment:
    """Helper class for click specific commands."""

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
