"""Unit tests for agent.
"""
from datetime import datetime

import unittest

from stock_trading_backend.agent import create_agent, FollowingFeatureAgent
from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file


class TestFollowingAgent(unittest.TestCase):
    """Unit tests for agent.
    """
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        features = [read_config_file("test/running_average_analysis.yaml")]
        agent = FollowingFeatureAgent(data_collection_config, features)
        self.assertEqual(data_collection_config, agent.data_collection_config)
        self.assertEqual("ra_5_stock_data_{}", agent.feature_template)

    def test_long_term(self):
        """A test for following feature agent 1 for 1 year.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2017, 1, 1)
        data_collection_config = read_config_file("data/default.yaml")
        agent_config = read_config_file("agent/following_feature_agent_1.yaml")
        agent = create_agent(agent_config, data_collection_config)
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date,
                                           min_start_balance=1000, max_start_balance=1000,
                                           max_stock_owned=1)
        observation = simulation.reset()
        while not simulation.done:
            observation, _, _ = simulation.step(agent.make_decision(observation, simulation))
        self.assertTrue(observation["net_worth"] >= 2500)

    def test_make_decision(self):
        """A test to see if make decision works properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data_collection_config = read_config_file("test/simulation.yaml")
        features = [read_config_file("test/running_average_analysis.yaml")]
        agent = FollowingFeatureAgent(data_collection_config, features)
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date,
                                           min_start_balance=100, max_start_balance=100,
                                           max_stock_owned=2)
        observation = simulation.reset()

        observation["ra_5_stock_data_GOOG"] = 0
        observation["ra_5_stock_data_AMZN"] = 0
        self.assertTrue(([0, 0] == agent.make_decision(observation, simulation)))

        observation["ra_5_stock_data_GOOG"] = 1
        observation["ra_5_stock_data_AMZN"] = 0
        self.assertTrue(([1, 0] == agent.make_decision(observation, simulation)))

        observation["ra_5_stock_data_GOOG"] = 1
        observation["ra_5_stock_data_AMZN"] = 1
        self.assertTrue(([1, 1] == agent.make_decision(observation, simulation)))

        observation, _, _ = simulation.step([1, 1])

        observation["ra_5_stock_data_GOOG"] = 1
        observation["ra_5_stock_data_AMZN"] = 1
        self.assertTrue(([0, 0] == agent.make_decision(observation, simulation)))

        observation["ra_5_stock_data_GOOG"] = 1
        observation["ra_5_stock_data_AMZN"] = 0
        self.assertTrue(([0, 1] == agent.make_decision(observation, simulation)))

        observation["ra_5_stock_data_GOOG"] = 0
        observation["ra_5_stock_data_AMZN"] = 0
        self.assertTrue(([1, 1] == agent.make_decision(observation, simulation)))

        observation["ra_5_stock_data_GOOG"] = 0
        observation["ra_5_stock_data_AMZN"] = 1
        self.assertTrue(([1, 0] == agent.make_decision(observation, simulation)))
