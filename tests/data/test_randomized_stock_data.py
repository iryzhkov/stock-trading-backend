"""Unit tests for randomized data.
"""
import unittest

from src.data import RandomizedStockData


class TestRandomizedStockData(unittest.TestCase):
    """Unit tests for randomized stock data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = RandomizedStockData()

    def test_a(self):
        """A simple test method.
        """
        self.assertFalse(self.data.data)
