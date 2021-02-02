"""Unit tests for comparator analysis.
"""
from datetime import datetime

import unittest

from parameterized import parameterized

from stock_trading_backend.data import ComparatorAnalysis, GeneratedStockData


class TestComparatorAnalysis(unittest.TestCase):
    """Unit tests for comparator analysis.
    """
    @parameterized.expand(["eq", "ne", "ge", "gt", "le", "lt"])
    def test_initializes(self, operator):
        """Tests if initializes properly.
        """
        data = ComparatorAnalysis(dependencies=["stock_data", "stock_data"], operator=operator)
        self.assertEqual("stock_data_{}_stock_data".format(operator), data.id_str)
        self.assertTrue(data.visible)

    def test_operator_error(self):
        """Tests if catches bed operator.
        """
        with self.assertRaises(ValueError):
            _ = ComparatorAnalysis(dependencies=["stock_data", "stock_data"], operator="??")

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 1, 1)
        stock_names = ["STOCK_1"]

        generated_data_1 = GeneratedStockData(evaluation_functions=["1"])
        generated_data_2 = GeneratedStockData(evaluation_functions=["2"])
        dependencies = [generated_data_1, generated_data_2]

        generated_data_1.prepare_data(from_date, to_date, stock_names, [])
        generated_data_2.prepare_data(from_date, to_date, stock_names, [])

        for operator in ["ge", "gt", "eq"]:
            comparator = ComparatorAnalysis(dependencies=["x", "x"], operator=operator)
            comparator.prepare_data(from_date, to_date, stock_names, dependencies)
            self.assertEqual(0, comparator[from_date].item())

        for operator in ["lt", "le", "ne"]:
            comparator = ComparatorAnalysis(dependencies=["x", "x"], operator=operator)
            comparator.prepare_data(from_date, to_date, stock_names, dependencies)
            self.assertEqual(1, comparator[from_date].item())
