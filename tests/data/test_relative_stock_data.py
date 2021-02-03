"""Unit tests for relative stock data.
"""
from datetime import datetime

import unittest
import numpy as np

from stock_trading_backend.data import RelativeStockData, GeneratedStockData


class TestRelativeStockData(unittest.TestCase):
    """Unit tests for relative stock data.
    """
    def test_initializes(self):
        """Tests if initializes properly.
        """
        data = RelativeStockData(dependencies=["stock_data"])
        self.assertEqual("relative_stock_data", data.id_str)
        self.assertFalse(data.visible)

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 1, 3)
        stock_names = ["STOCK_1"]
        value = 100
        dependency = GeneratedStockData(evaluation_functions=[str(value)])
        data = RelativeStockData(dependencies=["stock_data"])
        dependency.prepare_data(from_date, to_date, stock_names, [])
        dependency.data.iloc[1] = 200
        data.prepare_data(from_date, to_date, stock_names, [dependency])
        self.assertTrue(data.ready)
        self.assertTrue((stock_names == data.data.columns.tolist()))
        self.assertEqual(1, data.data.iloc[0].item())
        self.assertEqual(-0.5, data[to_date].item())

    def test_reset(self):
        """Tests if the data is reset properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 1, 3)
        stock_names = ["STOCK_1"]
        value = 100
        dependency = GeneratedStockData(evaluation_functions=[str(value)])
        data = RelativeStockData(dependencies=["stock_data"])
        dependency.prepare_data(from_date, to_date, stock_names, [])
        data.prepare_data(from_date, to_date, stock_names, [dependency])
        self.assertTrue(data.ready)
        data.reset([True])
        self.assertTrue(data.ready)
        data.reset([False])
        self.assertFalse(data.ready)

    def test_get_buffer(self):
        """Tests if the buffer is calculated properly.
        """
        data = RelativeStockData(dependencies=["stock_data"])
        data.buffer_days([5])
        self.assertEqual(6, data.buffer)
