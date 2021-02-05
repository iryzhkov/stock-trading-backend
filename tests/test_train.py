"""Unit tests for training.
"""
import unittest

from parameterized import parameterized

from stock_trading_backend import api
from stock_trading_backend.train import train_agent


class TestTraining(unittest.TestCase):
    """Unit tests for training.
    """
    @parameterized.expand([
        ("sarsa_learning_agent_0", "generated_1", "net_worth_ratio", "linear"),
    ])
    def test_training(self, agent_name, data_collection_name, reward_name, model_name):
        """Checks if training works.

        Args:
            agent_name: the agent to test training with.
            data_collection_name: the data collection to test training with.
            reward_name: the reward to test training with.
            model_name: the model to test training with.
        """
        agent = api.get_agent_object(agent_name, data_collection_name, reward_name, model_name)
        _, loss_history = train_agent(agent, episode_batch_size=2, num_episodes=4,
                                      min_duration=10, max_duration=20)
        self.assertTrue(loss_history[0] > loss_history[-1])
        self.assertTrue(agent.usable)

    def test_non_trainable_agent(self):
        """Test if providing non-trainable agent raises error.
        """
        agent = api.get_agent_object("following_feature_agent_1")
        with self.assertRaises(ValueError):
            _, _ = train_agent(agent)
