"""Unit tests for agent.
"""
from datetime import datetime

import unittest
import itertools

from stock_trading_backend.agent import FollowingFeatureAgent
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
        agent = FollowingFeatureAgent(data_collection_config=data_collection_config,
                                      reward_config=None, features=features)
        self.assertEqual(data_collection_config, agent.data_collection_config)
        self.assertEqual("ra_5_stock_data_{}", agent.feature_template)

    def test_make_decision(self):
        """A test to see if make decision works properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data_collection_config = read_config_file("test/simulation.yaml")
        features = [read_config_file("test/running_average_analysis.yaml")]
        agent = FollowingFeatureAgent(data_collection_config=data_collection_config,
                                      reward_config=None, features=features)
        simulation = StockMarketSimulation(data_collection_config, from_date, to_date,
                                           min_start_balance=100, max_start_balance=100,
                                           max_stock_owned=2)
        observation = simulation.reset()

        def check(val_1, val_2, exp_1, exp_2):
            observation["ra_5_stock_data_GOOG"] = val_1
            observation["ra_5_stock_data_AMZN"] = val_2
            expected = [exp_1, exp_2]
            action, _ = agent.make_decision(observation, simulation)
            self.assertTrue((expected == action))

        for i, j in itertools.combinations([0, 1], 2):
            check(i, j, i + 1, j + 1)

        observation, _, _ = simulation.step([2, 2])

        for i, j in itertools.combinations([0, 1], 2):
            check(i, j, i, j)
