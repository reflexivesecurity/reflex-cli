"""Module for the PackageGenerator class"""
import logging
import os
import shutil
import subprocess
import sys
import tempfile
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
        self.temp_dir = f"{tempfile.gettempdir()}/reflex_package"

    def generate_package(self, rule):
        """Creates a deployment package for the specified Rule.

        Args:
            rule (reflex_cli.Rule): The Reflex Rule to create a deployment package for
        """
        try:
            self.create_directories()
            self.download_zipped_codebase(rule)
            self.extract_zipped_codebase()
            self.build_package_contents()
            self.build_package_archive(rule)
        finally:
            self.clean_up()

    def create_directories(self):
        """Creates required directories."""
        try:
            os.mkdir(self.output_directory)
        except FileExistsError:
            LOGGER.debug("%s already exists", self.output_directory)

        LOGGER.debug("Creating temp directory")
        os.makedirs(self.temp_dir, exist_ok=True)

    def download_zipped_codebase(self, rule):
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
        with open(f"{self.temp_dir}/rule.zip", "wb") as source_codebase:
            source_codebase.write(response.content)

    def extract_zipped_codebase(self):
        """Extracts zipped codebase and deletes zip file."""
        LOGGER.debug("Extracting zip to temp")
        with zipfile.ZipFile(f"{self.temp_dir}/rule.zip", "r") as zip_file:
            zip_file.extractall(self.temp_dir)

        LOGGER.debug("Deleting %s/rule.zip", self.temp_dir)
        os.remove(f"{self.temp_dir}/rule.zip")

    def build_package_contents(self):
        """Runs pip install and builds python package."""
        # Get the rule directory name
        rule_directory = os.listdir(self.temp_dir)[0]

        LOGGER.debug(
            "Copying source files from %s/%s/source to %s/package",
            self.temp_dir,
            rule_directory,
            self.temp_dir,
        )
        shutil.copytree(
            f"{self.temp_dir}/{rule_directory}/source", f"{self.temp_dir}/package"
        )

        self.install_package_dependencies(f"{self.temp_dir}/package/requirements.txt")
        if self.additional_requirements:
            for requirements_file in self.additional_requirements:
                self.install_package_dependencies(requirements_file)

        if self.additional_files:
            for additional_file in self.additional_files:
                shutil.copy(additional_file, f"{self.temp_dir}/package/")

        # Remove requirements.txt from package directory
        os.remove(f"{self.temp_dir}/package/requirements.txt")

        # Overwrite AWSRule with custom AWSRule if desired
        if self.custom_rule_path:
            shutil.copy(
                self.custom_rule_path,
                f"{self.temp_dir}/package/reflex_core/aws_rule.py",
            )

    def install_package_dependencies(self, requirements_path):
        """Installs requirements from the specified requirements file using pip.

        Args:
            requirements_path (str): Path to a pip requirements file
        """
        LOGGER.debug(
            "Installing dependencies from %s into %s/package",
            requirements_path,
            self.temp_dir,
        )
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                requirements_path,
                "-t",
                f"{self.temp_dir}/package",
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
            f"{self.output_directory}/{rule.name}", "zip", f"{self.temp_dir}/package"
        )

    def clean_up(self):
        """Delete temp/ directory."""
        LOGGER.debug("Deleting %s", self.temp_dir)
        shutil.rmtree(self.temp_dir)
