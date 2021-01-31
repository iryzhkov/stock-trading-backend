"""Unit tests for stock market simulation.
"""
from datetime import datetime

import unittest

from src.simulation import StockMarketSimulation
from src.util import read_config_file


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def test_initializes(self):
        """Test for simulation initializtion.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data_collection_config = read_config_file("test/data_collection.yaml")
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date)
        self.assertEqual(0, simulation.max_start_balance)

    def test_resets(self):
        """Test for simulation reset.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data_collection_config = read_config_file("test/data_collection.yaml")
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date)
        simulation.reset()
        self.assertEqual(0, simulation.from_date_index)
        self.assertEqual(0, simulation.curr_date_index)
        self.assertEqual(16, simulation.to_date_index)

    def test_step(self):
        """Test for simulation step.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data_collection_config = read_config_file("test/data_collection.yaml")
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date)
        simulation.reset()
        _, reward, done = simulation.step([])
        self.assertFalse(done)
        self.assertEqual(0, reward)
