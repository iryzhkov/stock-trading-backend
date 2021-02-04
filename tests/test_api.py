"""Unit tests for API.
"""
from datetime import datetime

import unittest

from parameterized import parameterized

from stock_trading_backend import api
from stock_trading_backend.backtest import backtest_agent
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

    def test_get_agent_config(self):
        """Checks if get_agent_config works properly.
        """
        agent_config = api.get_agent_config("following_feature_agent_1")
        self.assertEqual("following_feature_agent", agent_config["name"])

    def test_get_available_data_collections(self):
        """Checks if get_data_collections works properly
        """
        available_data_collections = api.get_available_data_collections()
        self.assertEqual(3, len(available_data_collections))
        self.assertIn("default", available_data_collections)
        self.assertIn("real_stock_1", available_data_collections)
        self.assertIn("real_stock_2", available_data_collections)

    def test_get_data_collection_config(self):
        """Checks if get_data_collection_config works properly.
        """
        data_collection_config = api.get_data_collection_config("default")
        self.assertEqual(2, len(data_collection_config["stock_names"]))

    def test_get_available_rewards(self):
        """Checks if get_available_rewards works properly
        """
        available_rewards = api.get_available_rewards()
        self.assertEqual(3, len(available_rewards))
        self.assertIn("constant", available_rewards)
        self.assertIn("sharpe_ratio", available_rewards)
        self.assertIn("net_worth_ratio", available_rewards)

    def test_get_reward_config(self):
        """Checks if get_reward_config works properly.
        """
        reward_config = api.get_reward_config("sharpe_ratio")
        self.assertEqual("sharpe_ratio_reward", reward_config["name"])

    def test_get_available_models(self):
        """Checks if get_available_models works properly
        """
        available_models = api.get_available_models()
        self.assertEqual(1, len(available_models))
        self.assertIn("linear", available_models)

    def test_get_model_config(self):
        """Checks if get_model_config works properly.
        """
        model_config = api.get_model_config("linear")
        self.assertEqual("polynomial_model", model_config["name"])

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
        reward = backtest_agent(agent)
        self.assertTrue(reward > -0.5)

    def test_multiple_backtests(self):
        """Checks if can run the backtest multiple times on an agent.
        """
        agent = api.get_agent_object()
        reward = backtest_agent(agent)
        self.assertTrue(reward > -0.5)
        reward = backtest_agent(agent)
        self.assertTrue(reward > -0.5)

    def test_long_backtest(self):
        """Check how backtesting works for 4-year simulation.
        """
        agent = api.get_agent_object("following_feature_agent_1", "real_stock_2", "net_worth_ratio")
        reward = backtest_agent(agent, from_date=datetime(2014, 1, 1), to_date=datetime(2018, 1, 1))
        self.assertTrue(reward > 1.97)
