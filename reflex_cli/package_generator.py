"""Module for the PackageGenerator class"""
import logging
import os
import shutil
import subprocess
import sys
import zipfile

import requests

LOGGER = logging.getLogger(__name__)


class PackageGenerator:
    """Generates lambda packages for Reflex rules.
    """

    def __init__(self, output_directory, custom_rule_path):
        self.output_directory = output_directory
        self.custom_rule_path = custom_rule_path

    def generate_package(self, rule):
        LOGGER.info(
            "Getting zip from https://api.github.com/repos/%s/%s/zipball/%s",
            rule.github_org,
            rule.repository_name,
            rule.version,
        )
        response = requests.get(
            f"https://api.github.com/repos/{rule.github_org}/{rule.repository_name}/zipball/{rule.version}",
            allow_redirects=True,
        )

        LOGGER.debug("Creating temp directory")
        os.makedirs("temp", exist_ok=True)
        try:
            os.mkdir(self.output_directory)
        except FileExistsError:
            LOGGER.debug("temp directory already exists")

        LOGGER.debug("Writing zip to temp/rule.zip")
        open("temp/rule.zip", "wb").write(response.content)

        LOGGER.debug("Extracting zip to temp")
        with zipfile.ZipFile("temp/rule.zip", "r") as zip_file:
            zip_file.extractall("temp")

        LOGGER.debug("Deleting temp/rule.zip")
        os.remove("temp/rule.zip")

        # Get the rule directory name
        rule_directory = os.listdir("temp")[0]

        LOGGER.debug(
            "Copying source files from temp/%s/source to temp/package", rule_directory
        )
        shutil.copytree(f"temp/{rule_directory}/source", "temp/package")

        LOGGER.debug("Installing all dependencies into temp/package")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "temp/package/requirements.txt",
                "-t",
                "temp/package",
            ]
        )

        # Remove requirements.txt from package directory
        os.remove("temp/package/requirements.txt")

        # Overwrite AWSRule with custom AWSRule if desired
        if self.custom_rule_path:
            shutil.copy(self.custom_rule_path, "temp/package/reflex_core")

        LOGGER.info(
            "Creating zip package for %s: %s/%s.zip",
            rule.name,
            self.output_directory,
            rule.name,
        )
        shutil.make_archive(
            f"{self.output_directory}/{rule.name}", "zip", "temp/package"
        )

        LOGGER.debug("Deleting temp/")
        shutil.rmtree("temp")
