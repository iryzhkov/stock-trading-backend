"""Unit tests for simulation stock ownership data.
"""
from datetime import datetime

import unittest

from src.data import StockOwnershipData


class TestStockOwnershipData(unittest.TestCase):
    """Unit tests for simulation stock ownership data.
    """
    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_names = ["STOCK_1", "STOCK_2"]
        expected_columns = ["owned_STOCK_1", "owned_STOCK_2"]
        data = StockOwnershipData()
        data.prepare_data(from_date, to_date, stock_names, [])
        self.assertTrue(data.ready)
        print(data.data)
        self.assertTrue((expected_columns == data.data.columns.tolist()))
        self.assertEqual(32, len(data))

    def test_reset_data(self):
        """Tests if the data is reset properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2020, 1, 1)
        stock_names = ["STOCK_1", "STOCK_2"]
        data = StockOwnershipData()
        data.prepare_data(from_date, to_date, stock_names, [])
        self.assertTrue(data.ready)
        data.reset([])
        self.assertFalse(data.ready)
