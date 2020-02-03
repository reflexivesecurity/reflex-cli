import os
import unittest

from reflex_cli.reflex_initializer import ReflexInitializer


class ReflexInitializerTestCase(unittest.TestCase):
    """Test class for the environment context of our CLI tool."""

    def setUp(self):
        self.initializer = ReflexInitializer(os.getcwd())

    def test_query_possible_measures(self):
        """Test our logic for measures is correct"""
