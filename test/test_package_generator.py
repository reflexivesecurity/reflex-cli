import os
import unittest
import shutil
from unittest.mock import MagicMock, patch

from reflex_cli.package_generator import PackageGenerator

OUTPUT_DIRECTORY = os.getcwd()

class PackageGeneratorTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.generator = PackageGenerator(OUTPUT_DIRECTORY, None)

    @patch(
        "reflex_cli.package_generator.requests.get"
    )
    def test_download_zipped_codebase(self, requests_mock):
        rule_mock = MagicMock()
        rule_mock.repository_name = "example"
        rule_mock.version = "0.0.1"
        rule_mock.github_org = "example"
        content_mock = MagicMock()
        content_mock.content = b"test"
        requests_mock.return_value = content_mock
        self.assertFalse(os.path.exists("temp/rule.zip"))
        self.generator.download_zipped_codebase(rule_mock)
        self.assertTrue(os.path.exists("temp/rule.zip"))
        shutil.rmtree(OUTPUT_DIRECTORY + "/temp/")
