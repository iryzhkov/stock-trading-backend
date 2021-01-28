"""Unit tests for data.
"""
import unittest

from parameterized import parameterized

from src.data import create_data, GeneratedStockData, RandomizedStockData, RealStockData
from src.data import RunningAverageAnalysis
from src.util import read_config_file


class TestDataFactory(unittest.TestCase):
    """Unit tests for data factory.
    """
    @parameterized.expand([
        ("test/generated_stock_data.yaml", GeneratedStockData),
        ("test/randomized_stock_data.yaml", RandomizedStockData),
        ("test/real_stock_data.yaml", RealStockData),
        ("test/running_average_analysis.yaml", RunningAverageAnalysis),
    ])
    def test_creates_data(self, config_filename, expected_class):
        """Checks if created data class is of the right class.
        """
        created_data = create_data(read_config_file(config_filename))
        self.assertIsInstance(created_data, expected_class)
