"""Tests for reflex_cli/package_generator.py"""
import os
import unittest

from reflex_cli.package_generator import PackageGenerator
from reflex_cli.rule import Rule

OUTPUT_DIRECTORY = os.getcwd()


class PackageGeneratorTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.generator = PackageGenerator(OUTPUT_DIRECTORY, None, [], [])
        self.rule = Rule(
            "s3-bucket-not-encrypted",
            {"configuration": {"mode": "detect"}, "version": "v1.0.0"},
        )

    def tearDown(self):
        os.remove("s3-bucket-not-encrypted.zip")

    def test_generate_package(self):
        """Test that generate_package creates the expected zip package."""
        self.generator.generate_package(self.rule)
        assert os.path.isfile("s3-bucket-not-encrypted.zip")
