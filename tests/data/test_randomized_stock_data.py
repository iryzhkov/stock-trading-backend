"""Unit tests for randomized data.
"""
import unittest

from src.data import RandomizedStockData


class TestRandomizedStockData(unittest.TestCase):
    """Unit tests for randomized stock data.
    """
    def test_id_str(self):
        """Tests if the id_str is correct.
        """
        data = RandomizedStockData(dependencies=["stock_data"])
        self.assertEqual("randomized_stock_data", data.id_str)

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        data = RandomizedStockData(dependencies=["stock_data"])
        data.prepare_data(None, None, None, None)
