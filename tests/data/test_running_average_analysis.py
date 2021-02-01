"""Unit tests for running average analysis.
"""
from datetime import datetime

import unittest

from stock_trading_backend.data import RunningAverageAnalysis, GeneratedStockData


class TestRunningAverageAnalysis(unittest.TestCase):
    """Unit tests for running average analysis.
    """
    def test_initializes(self):
        """Tests if initializes properly.
        """
        data = RunningAverageAnalysis(dependencies=["stock_data"])
        self.assertEqual("running_average_1_for_stock_data", data.id_str)
        self.assertTrue(data.visible)

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        num_days = 5
        stock_names = ["STOCK_1", "STOCK_2"]
        expected_columns = ["ra_5_stock_data_STOCK_1", "ra_5_stock_data_STOCK_2"]

        dependency = GeneratedStockData(evaluation_functions=["100"])
        data = RunningAverageAnalysis(dependencies=["stock_data"], num_days=num_days)
        dependency.prepare_data(from_date, to_date, stock_names, [])
        data.prepare_data(from_date, to_date, stock_names, [dependency])

        self.assertTrue(data.ready)
        self.assertTrue((expected_columns == data.data.columns.tolist()))
        self.assertEqual(len(dependency) - num_days + 1, len(data))
        self.assertEqual(100, data[to_date][0])

    def test_resets_data(self):
        """Tests if the data is reset properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2020, 1, 1)
        stock_names = ["STOCK_1"]
        dependency = GeneratedStockData(evaluation_functions=["100"])
        data = RunningAverageAnalysis(dependencies=["stock_data"])
        dependency.prepare_data(from_date, to_date, stock_names, [])
        data.prepare_data(from_date, to_date, stock_names, [dependency])
        self.assertTrue(data.ready)
        data.reset([True])
        self.assertTrue(data.ready)

    def test_buffer_days(self):
        """Tests if number of buffer days is calculated.
        """
        data = RunningAverageAnalysis(dependencies=["stock_data"], num_days=30)
        data.buffer_days([0])
        self.assertEqual(30, data.buffer)
