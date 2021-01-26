"""Unit tests for real stock data.
"""
import unittest

from src.data import RealStockData


class TestRealStockData(unittest.TestCase):
    """Unit tests for real stock data data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = RealStockData()

    def test_a(self):
        """A simple test method.
        """
        self.assertTrue(True)
