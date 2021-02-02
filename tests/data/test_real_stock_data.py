"""Unit tests for real stock data.
"""
from datetime import datetime

import unittest

from stock_trading_backend.data import RealStockData


class TestRealStockData(unittest.TestCase):
    """Unit tests for real stock data data.
    """
    def test_initializes(self):
        """Tests if initializes properly.
        """
        data = RealStockData()
        self.assertFalse(data.visible)

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        stock_names = ["GOOG", "AAPL"]
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        dependencies = []

        data = RealStockData()
        data.prepare_data(from_date, to_date, stock_names, dependencies)
        self.assertTrue(data.ready)
        self.assertTrue((stock_names == data.data.columns.tolist()))
        self.assertEqual(20, len(data))

    def test_resets_data(self):
        """Tests if the data is reset properly.
        """
        stock_names = ["GOOG", "AAPL"]
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        dependencies = []

        data = RealStockData()
        data.prepare_data(from_date, to_date, stock_names, dependencies)
        self.assertTrue(data.ready)
        data.reset([])
        self.assertTrue(data.ready)
