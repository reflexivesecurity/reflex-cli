import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.template_generator import TemplateGenerator

EXAMPLE_CONFIG = {
    "version": 0.1,
    "globals": {"default_email": "john@example.com"},
    "providers": ["aws"],
    "rules": [
        "aws-detect-root-user-activity",
        {"aws-detect-deactivate-mfa": {"email": "john.smith@example.com"}},
        "aws-enforce-no-public-ami",
        "aws-enforce-s3-encryption",
        {"aws-detect-pants-on-fire": {"url": "github.com/example/pants"}},
    ],
}

OUTPUT_DIRECTORY = os.getcwd()


class TemplateGeneratorTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.generator = TemplateGenerator(EXAMPLE_CONFIG, OUTPUT_DIRECTORY)

    def test_generate_template(self):
        get_template_mock = MagicMock()
        render_mock = MagicMock()
        render_mock.render.return_value = "Example"
        get_template_mock.get_template.return_value = render_mock
        self.generator.template_env = get_template_mock
        self.assertEqual(
            self.generator.generate_template(
                "test", {"test": {"version": "0.0.0.1"}}
            ),
            "Example",
        )

    @patch(
        "reflex_cli.template_generator.TemplateGenerator.write_template_file"
    )
    def test_write_template_file(self, write_template_file_mock):
        write_template_file_mock.return_value = True
