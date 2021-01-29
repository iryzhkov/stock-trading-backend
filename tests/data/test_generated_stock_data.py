"""Unit tests for generated stock data.
"""
import unittest

from src.data import GeneratedStockData


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        data = GeneratedStockData()
        data.prepare_data(None, None, None, None)
        self.assertTrue(data.ready)
