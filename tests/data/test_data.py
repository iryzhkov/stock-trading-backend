"""Unit tests for data.
"""
import unittest

from src.data import Data


class TestData(unittest.TestCase):
    """Unit tests for data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = Data()

    def test_a(self):
        """A simple test method.
        """
        self.assertFalse(self.data.data)
