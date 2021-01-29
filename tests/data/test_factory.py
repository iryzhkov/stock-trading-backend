"""Unit tests for data factory.
"""
import unittest

from parameterized import parameterized

from src.data import create_data, GeneratedStockData, RandomizedStockData, RealStockData
from src.data import RunningAverageAnalysis, create_data_collection, DataCollection
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

        Args:
            config_filename: the filename for the config file.
            expected_class: the expected class created from config file.
        """
        data = create_data(read_config_file(config_filename))
        self.assertIsInstance(data, expected_class)

    def test_creates_data_collection(self):
        """Checks if creates data collection.
        """
        data_collection = create_data_collection(read_config_file("test/data_collection.yaml"))
        self.assertIsInstance(data_collection, DataCollection)
