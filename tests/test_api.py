"""Unit tests for API.
"""
import unittest

from stock_trading_backend import api
from stock_trading_backend.agent import FollowingFeatureAgent

class TestAPI(unittest.TestCase):
    """Unit tests for api.
    """
    def test_get_available_agents(self):
        """Checks if get_agent_names works properly
        """
        available_agents = api.get_available_agents()
        self.assertEqual(2, len(available_agents))
        self.assertIn("following_feature_agent_1", available_agents)
        self.assertIn("sarsa_learning_agent_1", available_agents)

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
