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
        to_date = datetime(2016, 1, 5)
        data_collection_config = read_config_file("test/simulation.yaml")
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date,
                                           min_start_balance=100, max_start_balance=100,
                                           max_stock_owned=2)
        _ = simulation.reset()

        observation, _, done = simulation.step([1, 0])
        self.assertEqual(50, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(5, observation["owned_GOOG"])
        self.assertEqual(0, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([0, 1])
        self.assertEqual(10, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(5, observation["owned_GOOG"])
        self.assertEqual(2, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([1, 0])
        self.assertEqual(60, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(0, observation["owned_GOOG"])
        self.assertEqual(2, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([0, 1])
        self.assertEqual(100, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(0, observation["owned_GOOG"])
        self.assertEqual(0, observation["owned_AMZN"])
        self.assertTrue(done)
