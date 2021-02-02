"""Unit tests for API.
"""
from datetime import datetime

import unittest

from parameterized import parameterized

from stock_trading_backend import api
from stock_trading_backend.agent import FollowingFeatureAgent

class TestAPI(unittest.TestCase):
    """Unit tests for api.
    """
    def test_get_available_agents(self):
        """Checks if get_agent_names works properly
        """
        available_agents = api.get_available_agents()
        self.assertEqual(1, len(available_agents))
        self.assertEqual("following_feature_agent_1", available_agents[0])

    def test_get_available_data_collections(self):
        """Checks if get_available_agents works properly
        """
        available_data_collections = api.get_available_data_collections()
        self.assertEqual(2, len(available_data_collections))
        self.assertIn("default", available_data_collections)
        self.assertIn("real_stock_1", available_data_collections)

    def test_get_agent_object(self):
        """Checks if get_agent_object works properly
        """
        agent = api.get_agent_object("following_feature_agent_1", "default")
        self.assertIsInstance(agent, FollowingFeatureAgent)

    @parameterized.expand([
        ("following_feature_agent_1", "default"),
        ("following_feature_agent_1", "real_stock_1"),
    ])
    def test_backtest(self, agent_name, data_collection_name):
        """Checks if backtesting works.

        Args:
            agent_name: the agent to test backtesting with.
            data_collection_name: the data collection to test backtesting with.
        """
        agent = api.get_agent_object(agent_name, data_collection_name)
        observation = api.backtest_agent(agent)
        self.assertTrue(observation["net_worth"] > 0)

    def test_long_backtest(self):
        """Check how backtesting works for 4-year simulation.
        """
        agent = api.get_agent_object("following_feature_agent_1")
        observation = api.backtest_agent(agent, from_date=datetime(2014, 1, 1),
                                         to_date=datetime(2018, 1, 1))
        self.assertTrue(observation["net_worth"] > 0)