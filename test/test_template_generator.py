import unittest
from unittest.mock import MagicMock
import os
from reflex_cli.template_generator import TemplateGenerator

EXAMPLE_CONFIGURATION = {
        'version': 0.1,
        'default_notification_email': 'john@example.com',
        'providers': ['aws'],
        'measures': ['aws-detect-root-user-activity',
                     {'aws-detect-deactivate-mfa':
                         {'email': 'john.smith@example.com'}},
                     'aws-enforce-no-public-ami',
                     'aws-enforce-s3-encryption',
                     {'aws-detect-pants-on-fire':
                         {'url': 'github.com/example/pants-on-fire'}}
                     ]
        }

OUTPUT_DIRECTORY = os.getcwd()


class TemplateGeneratorTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""
    def setUp(self):
        self.generator = TemplateGenerator(EXAMPLE_CONFIGURATION,
                                           OUTPUT_DIRECTORY)

    def test_determine_template_name(self):
        """Test our defaults for the environment are sane."""
        string_test = self.generator.determine_template_name('test_template')
        self.assertEqual(string_test, 'test_template.tf')
        test_dict = {'test_template': {'one': 'first'}}
        dict_test = self.generator.determine_template_name(test_dict)
        self.assertEqual(dict_test, 'test_template.tf')
