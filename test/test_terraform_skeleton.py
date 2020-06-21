import os
import unittest
from unittest.mock import MagicMock, patch

from reflex_cli.terraform_skeleton import TerraformSkeleton


class TerraformSkeletonTestCase(unittest.TestCase):
    @patch("reflex_cli.terraform_skeleton.RuleDiscoverer.collect_engine")
    def setUp(self, rule_discoverer_mock):
        rule_discoverer_mock.return_value = {
            "reflex-engine": {"version": "v1.0.0"}
        }
        configuration_object = {
            "rule_name": "unit-test-rule",
            "class_name": "UnitTestRule",
            "mode": "detect",
        }
        self.terraform_skeleton = TerraformSkeleton(
            output_directory="test_dir", configuration=configuration_object
        )

    @patch("reflex_cli.terraform_skeleton.write_template_file")
    def test_create_template(self, write_template_file):
        self.terraform_skeleton.create_template(
            "cwe.tf",
            {
                "rule_class_name": self.terraform_skeleton.class_name,
                "engine_version": self.terraform_skeleton.engine_version,
            },
            "terraform/cwe/cwe.tf",
        )
        write_template_file.assert_called_once()
