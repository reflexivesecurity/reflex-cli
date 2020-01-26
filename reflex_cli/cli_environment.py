"""Class to create decorator for command classes."""
import os


class CliEnvironment:
    """Helper class for click specific commands."""

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
