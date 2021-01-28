"""Unit tests for file utils.
"""
import unittest

from src.util import read_config_file


class TestFileUtilsData(unittest.TestCase):
    """Unit tests for file utils.
    """
    def test_config_reader(self):
        """Unit test for config reader.
        """
        config = read_config_file("test/test_config.yaml")
        self.assertEqual(type({}), type(config))
        self.assertIn("test", config)
        self.assertEqual("test", config["test"])
