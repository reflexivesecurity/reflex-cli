""" Remove repeated path functions into own file. """

import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def ensure_output_directory_exists(output_directory):  # pragma: no cover
    """Ensure that the path to the output directory exists."""
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    directory_list = [
        "/source",
        "/.github/workflows",
        "/terraform/cwe",
        "/terraform/sqs_lambda",
    ]
    for directory in directory_list:
        Path(output_directory + directory).mkdir(parents=True, exist_ok=True)


def write_template_file(output_file, rendered_template):  # pragma: no cover
    """Writes output of rendering to file"""
    LOGGER.info("Creating %s", output_file)
    with open(output_file, "w+") as file_handler:
        file_handler.write(rendered_template)
