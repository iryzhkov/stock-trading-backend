"""Unit tests for generated stock data.
"""
import unittest

from src.data import GeneratedStockData


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = GeneratedStockData()

    def test_a(self):
        """A simple test method.
        """
        self.assertFalse(self.data.data)
