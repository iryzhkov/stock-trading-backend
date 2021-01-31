"""Unit tests for generated stock data.
"""
from datetime import datetime

import unittest

from src.data import GeneratedStockData


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def test_requires_evaluation_functions(self):
        """Tests if raises exception when no evaluation functions are provided.
        """
        with self.assertRaises(ValueError):
            _ = GeneratedStockData()

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_names = ["STOCK_1", "STOCK_2"]
        data = GeneratedStockData(evaluation_functions=["100", "200"])
        data.prepare_data(from_date, to_date, stock_names, [])
        self.assertTrue(data.ready)
        self.assertTrue((stock_names == data.data.columns.tolist()))
        self.assertEqual(100, data[from_date][0])
        self.assertEqual(200, data[from_date][1])

    def test_resets_data(self):
        """Tests if the data is reset properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_names = ["STOCK_1", "STOCK_2"]
        data = GeneratedStockData(evaluation_functions=["100"])
        data.prepare_data(from_date, to_date, stock_names, [])
        self.assertTrue(data.ready)
        data.reset([])
        self.assertTrue(data.ready)
