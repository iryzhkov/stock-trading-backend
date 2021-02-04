"""Unit tests for stock market simulation.
"""
from datetime import datetime

import unittest

import gym

from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file


class TestStockMarketSimulation(unittest.TestCase):
    """Unit tests for stock market simulation.
    """
    def test_initializes(self):
        """Test for simulation initialization.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data_collection_config = read_config_file("test/data_collection.yaml")
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date)
        self.assertEqual(1000, simulation.max_start_balance)

    def test_default_initialization(self):
        """Test for default simulation initialization.
        """
        simulation = StockMarketSimulation()
        self.assertEqual(1000, simulation.max_start_balance)
        self.assertEqual(732, len(simulation.available_dates))

    def test_action_space_generator(self):
        """Test if action space generator works properly.
        """
        simulation = StockMarketSimulation()
        simulation.reset()

        # 3 possible actions: [0, 0], [1, 0], [1, 1]
        self.assertEqual(3, len(list(simulation.action_space_generator())))
        for action in simulation.action_space_generator():
            self.assertEqual(2, len(action))

        # 2 possible actions: [0, 0], [1, 0]
        simulation.owned_stocks[0] = 1
        self.assertEqual(2, len(list(simulation.action_space_generator())))
        for action in simulation.action_space_generator():
            self.assertEqual(2, len(action))

        # 4 possible actions: [0, 0], [1, 0], [0, 1], [1, 1]
        simulation.max_stock_owned = 2
        self.assertEqual(4, len(list(simulation.action_space_generator())))
        for action in simulation.action_space_generator():
            self.assertEqual(2, len(action))

    def test_initializes_from_gym(self):
        """Test if simulation can be initialized with gym.make()
        """
        simulation = gym.make("stock-market-v0")
        self.assertIsInstance(simulation, StockMarketSimulation)
        self.assertEqual(1000, simulation.max_start_balance)
        self.assertEqual(732, len(simulation.available_dates))

    def test_initializes_from_gym_with_parameters(self):
        """Test if simulation can be initialized with gym.make()
        """
        simulation = gym.make("stock-market-v0", max_start_balance=500)
        self.assertIsInstance(simulation, StockMarketSimulation)
        self.assertEqual(500, simulation.max_start_balance)

    def test_weird_date_range(self):
        """Test simulation initialization with half of the date range.
        """
        date = datetime(2016, 1, 1)
        with self.assertRaises(ValueError):
            _ = StockMarketSimulation(from_date=date)
        with self.assertRaises(ValueError):
            _ = StockMarketSimulation(to_date=date)

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

    def test_reward_is_used(self):
        """Test if reward config is used in initialization funciton.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 1, 5)
        data_collection_config = read_config_file("test/simulation.yaml")
        reward_config = {"name": "constant_reward", "value": 5}
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date,
                                           min_start_balance=100, max_start_balance=100,
                                           max_stock_owned=2, reward_config=reward_config)
        _ = simulation.reset()
        _, reward, _ = simulation.step([0, 0])
        self.assertEqual(5, reward)
        self.assertEqual(5, simulation.overall_reward)

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
        self.assertEqual(60, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(2, observation["owned_GOOG"])
        self.assertEqual(0, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([0, 1])
        self.assertEqual(0, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(2, observation["owned_GOOG"])
        self.assertEqual(6, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([1, 0])
        self.assertEqual(40, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(0, observation["owned_GOOG"])
        self.assertEqual(6, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([0, 1])
        self.assertEqual(100, observation["balance"])
        self.assertEqual(100, observation["net_worth"])
        self.assertEqual(0, observation["owned_GOOG"])
        self.assertEqual(0, observation["owned_AMZN"])
        self.assertTrue(done)

    def test_too_expensive(self):
        """Test for ignoring expensive purchases.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 1, 5)
        data_collection_config = read_config_file("test/simulation.yaml")
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date,
                                           min_start_balance=10, max_start_balance=10,
                                           max_stock_owned=1)
        _ = simulation.reset()

        observation, _, done = simulation.step([1, 1])
        self.assertEqual(0, observation["balance"])
        self.assertEqual(10, observation["net_worth"])
        self.assertEqual(0, observation["owned_GOOG"])
        self.assertEqual(1, observation["owned_AMZN"])
        self.assertFalse(done)

        observation, _, done = simulation.step([1, 0])
        self.assertEqual(0, observation["balance"])
        self.assertEqual(10, observation["net_worth"])
        self.assertEqual(0, observation["owned_GOOG"])
        self.assertEqual(1, observation["owned_AMZN"])
        self.assertFalse(done)
