"""Unit tests for randomized data.
"""
from datetime import datetime

import unittest
import numpy as np

from src.data import RandomizedStockData, GeneratedStockData


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
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2020, 1, 1)
        stock_names = ["STOCK_1"]
        value = 100
        mean = 0.05
        stdev = 0.025
        dependency = GeneratedStockData(evaluation_functions=[str(value)])
        data = RandomizedStockData(dependencies=["stock_data"], mean=mean, stdev=stdev)
        dependency.prepare_data(from_date, to_date, stock_names, [])
        data.prepare_data(from_date, to_date, stock_names, [dependency])
        self.assertTrue(data.ready)
        self.assertTrue((stock_names == data.data.columns.tolist()))
        self.assertTrue(np.isclose(value * (1 + mean), data.data["STOCK_1"].mean(), rtol=0.05))
        self.assertTrue(np.isclose(value * stdev, data.data["STOCK_1"].std(), rtol=0.05))

    def test_resets_data(self):
        """Tests if the data is reset properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 3, 1)
        stock_names = ["STOCK_1"]
        value = 100
        mean = 0.05
        stdev = 0.025
        dependency = GeneratedStockData(evaluation_functions=[str(value)])
        data = RandomizedStockData(dependencies=["stock_data"], mean=mean, stdev=stdev)
        dependency.prepare_data(from_date, to_date, stock_names, [])
        data.prepare_data(from_date, to_date, stock_names, [dependency])

        data_before_reset = data.data["STOCK_1"].copy()

        self.assertTrue(data.ready)
        data.reset([True])
        self.assertFalse(data.ready)

        data.prepare_data(from_date, to_date, stock_names, [dependency])
        data_after_reset = data.data["STOCK_1"]
        self.assertFalse(data_before_reset.equals(data_after_reset))
