"""Unit tests for agent.
"""
from datetime import datetime

import unittest

from stock_trading_backend.agent import Agent
from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file


class TestAgent(unittest.TestCase):
    """Unit tests for agent.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        self.data_collection_config = read_config_file("test/simulation.yaml")
        self.simulation = StockMarketSimulation(self.data_collection_config, from_date, to_date,
                                                min_start_balance=100, max_start_balance=100,
                                                max_stock_owned=2)
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        agent = Agent(self.data_collection_config, None)
        self.assertEqual(self.data_collection_config, agent.data_collection_config)
        self.assertTrue(agent.usable)

    def test_observation_unpack(self):
        """A test to see if observation unpack works.
        """
        agent = Agent(self.data_collection_config, None)
        observation = self.simulation.reset()
        balance, net_worth, owned_stocks, stock_prices = agent.unpack_observation(observation)
        self.assertEqual(100, balance)
        self.assertEqual(100, net_worth)
        self.assertTrue(([0, 0] == owned_stocks))
        self.assertTrue(([20, 10] == stock_prices))

        observation, _, _ = self.simulation.step([2, 2])
        balance, net_worth, owned_stocks, stock_prices = agent.unpack_observation(observation)
        self.assertEqual(10, balance)
        self.assertEqual(100, net_worth)
        self.assertTrue(([1, 1] == owned_stocks))
        self.assertTrue(([20, 10] == stock_prices))

    def test_make_decision(self):
        """A test to see if agent can make decisions.
        """
        agent = Agent(self.data_collection_config, None)
        observation = self.simulation.reset()

        while not self.simulation.done:
            action, _ = agent.make_decision(observation, self.simulation)
            self.assertEqual(2, len(action))
            observation, _, _ = self.simulation.step(action)
            _, net_worth, _, _ = agent.unpack_observation(observation)
            self.assertEqual(100, net_worth)

    def test_save_and_load(self):
        """A test to see if agent uses save and load properly.
        """
        agent = Agent(self.data_collection_config)
        self.assertTrue(agent.can_be_loaded())
        agent.save()
        self.assertTrue(agent.can_be_loaded())
        agent.load()
        self.assertTrue(agent.can_be_loaded())

    def test_load_lookup_error(self):
        """A test to see if look up error works properly.
        """
        agent = Agent(self.data_collection_config)
        agent.requires_learning = True
        with self.assertRaises(LookupError):
            agent.load()

    def test_id_str_with_hash(self):
        """A test to see if agent id str with hash is set up properly.
        """
        agent = Agent(self.data_collection_config, None)
        self.assertEqual(4, len(agent.id_str_with_hash.split("_")))
