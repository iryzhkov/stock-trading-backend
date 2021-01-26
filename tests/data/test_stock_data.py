"""Unit tests for stock data.
"""
import unittest

from src.data import StockData


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for stock data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = StockData()

    def test_a(self):
        """A simple test method.
        """
        self.assertTrue(True)
