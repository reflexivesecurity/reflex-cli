import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.repo_foundation_skeleton import RepoFoundationSkeleton


class RepoFoundationSkeletonTestCase(unittest.TestCase):
    def setUp(self):
        configuration_object = {
            "github_org": "test",
            "rule_name": "unit-test-rule",
            "class_name": "UnitTestRule",
            "mode": "detect",
        }
        self.repo_foundation_skeleton = RepoFoundationSkeleton(
            output_directory="test_dir", configuration=configuration_object
        )

    @patch("reflex_cli.repo_foundation_skeleton.write_template_file")
    def test_create_template(self, write_template_file):
        self.repo_foundation_skeleton.create_template(
            "source/rule.py.jinja2",
            {
                "rule_class_name": self.repo_foundation_skeleton.class_name,
                "mode": self.repo_foundation_skeleton.mode,
            },
            f"source/{self.repo_foundation_skeleton.rule_name.replace('-','_')}.py",
        )
        write_template_file.assert_called_once()
