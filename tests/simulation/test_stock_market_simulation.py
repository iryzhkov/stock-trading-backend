"""Unit tests for stock market simulation.
"""
import unittest

from src.simulation import StockMarketSimulation
from src.util import read_config_file


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def test_initializes(self):
        """Test for simulation initializtion.
        """
        data_collection_config = read_config_file("test/data_collection.yaml")
        simulation = StockMarketSimulation(data_collection_config)
        self.assertEqual(0, simulation.max_start_balance)
