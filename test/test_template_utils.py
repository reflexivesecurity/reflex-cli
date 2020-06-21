import unittest
from unittest.mock import  patch, mock_open

from reflex_cli.create_template_utils import ensure_output_directory_exists, write_template_file


class TemplateUtilsTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    @patch('pathlib.Path.mkdir')
    def test_create_rule_list(self, mock_mkdir):
        ensure_output_directory_exists("/test")
        mock_mkdir.assert_called_with(parents=True, exist_ok=True)

    def test_write_template_file(self):
        with patch("builtins.open", mock_open()) as open_mock:
            write_template_file("test.txt", "test")
            open_mock.assert_called_with('test.txt', 'w+')
            open_mock.return_value.write.assert_called_with("test")

