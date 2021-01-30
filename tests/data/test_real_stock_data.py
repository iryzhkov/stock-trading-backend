"""Unit tests for real stock data.
"""
import unittest

from src.data import RealStockData


class TestRealStockData(unittest.TestCase):
    """Unit tests for real stock data data.
    """
    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        data = RealStockData()
        data.prepare_data(None, None, None, None)
        self.assertTrue(data.ready)

    def test_resets_data(self):
        """Tests if the data is reset properly.
        """
        data = RealStockData()
        data.prepare_data(None, None, None, None)
        self.assertTrue(data.ready)
        data.reset([])
        self.assertTrue(data.ready)
