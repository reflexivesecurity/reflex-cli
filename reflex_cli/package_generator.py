"""Module for the PackageGenerator class"""
import logging
import os
import shutil
import subprocess
import sys
import zipfile

import requests

LOGGER = logging.getLogger(__name__)


class PackageGenerator:  # pylint: disable=too-few-public-methods
    """Generates lambda packages for Reflex rules."""

    def __init__(
        self,
        output_directory,
        custom_rule_path,
        additional_requirements,
        additional_files,
    ):
        self.output_directory = output_directory
        self.custom_rule_path = custom_rule_path
        self.additional_requirements = additional_requirements
        self.additional_files = additional_files

    def generate_package(self, rule):
        """Creates a deployment package for the specified Rule.

        Args:
            rule (reflex_cli.Rule): The Reflex Rule to create a deployment package for
        """
        self.create_directories()
        self.download_zipped_codebase(rule)
        self.extract_zipped_codebase()
        self.build_package_contents()
        self.build_package_archive(rule)
        self.clean_up()

    def create_directories(self):
        """Creates required directories."""
        LOGGER.debug("Creating temp directory")
        os.makedirs("temp", exist_ok=True)
        try:
            os.mkdir(self.output_directory)
        except FileExistsError:
            LOGGER.debug("temp directory already exists")

    @staticmethod
    def download_zipped_codebase(rule):
        """Pulls full codebase down as zip from GitHub."""
        LOGGER.info(
            "Getting zip from https://api.github.com/repos/%s/%s/zipball/%s",
            rule.github_org,
            rule.repository_name,
            rule.version,
        )
        response = requests.get(
            f"https://api.github.com/repos/{rule.github_org}/{rule.repository_name}/zipball/{rule.version}",  # pylint: disable=line-too-long
            allow_redirects=True,
        )
        LOGGER.debug("Writing zip to temp/rule.zip")
        with open("temp/rule.zip", "wb") as source_codebase:
            source_codebase.write(response.content)

    @staticmethod
    def extract_zipped_codebase():
        """Extracts zipped codebase and deletes zip file."""
        LOGGER.debug("Extracting zip to temp")
        with zipfile.ZipFile("temp/rule.zip", "r") as zip_file:
            zip_file.extractall("temp")

        LOGGER.debug("Deleting temp/rule.zip")
        os.remove("temp/rule.zip")

    def build_package_contents(self):
        """Runs pip install and builds python package."""
        # Get the rule directory name
        rule_directory = os.listdir("temp")[0]

        LOGGER.debug(
            "Copying source files from temp/%s/source to temp/package", rule_directory
        )
        shutil.copytree(f"temp/{rule_directory}/source", "temp/package")

        self.install_package_dependencies("temp/package/requirements.txt")
        if self.additional_requirements:
            for requirements_file in self.additional_requirements:
                self.install_package_dependencies(requirements_file)

        if self.additional_files:
            for additional_file in self.additional_files:
                shutil.copy(additional_file, "temp/package/")

        # Remove requirements.txt from package directory
        os.remove("temp/package/requirements.txt")

        # Overwrite AWSRule with custom AWSRule if desired
        if self.custom_rule_path:
            shutil.copy(self.custom_rule_path, "temp/package/reflex_core/aws_rule.py")

    @staticmethod
    def install_package_dependencies(requirements_path):
        """Installs requirements from the specified requirements file using pip.

        Args:
            requirements_path (str): Path to a pip requirements file
        """
        LOGGER.debug("Installing dependencies from %s into temp/package", requirements_path)
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                requirements_path,
                "-t",
                "temp/package",
            ]
        )

    def build_package_archive(self, rule):
        """Creates built zip package for deployment."""
        LOGGER.info(
            "Creating zip package for %s: %s/%s.zip",
            rule.name,
            self.output_directory,
            rule.name,
        )
        shutil.make_archive(
            f"{self.output_directory}/{rule.name}", "zip", "temp/package"
        )

    @staticmethod
    def clean_up():
        """Delete temp/ directory."""
        LOGGER.debug("Deleting temp/")
        shutil.rmtree("temp")
