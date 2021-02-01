"""Unit tests for reward factory.
"""
import unittest

from parameterized import parameterized

from stock_trading_backend.simulation import create_reward, StockMarketSimulation
from stock_trading_backend.simulation.reward import Reward

class TestRewardFactory(unittest.TestCase):
    """Tests for reward factory.
    """
    @parameterized.expand([
        ({"name": "constant"}, Reward),
    ])
    def test_creates_correct_class(self, reward_config, expected_class):
        """Tests if creat_reward creates the correct class.
        """
        simulation = StockMarketSimulation()
        reward = create_reward(reward_config, simulation)
        self.assertIsInstance(reward, expected_class)

    def test_raises_lookup_error(self):
        """Tests if creat_reward raises lookup error when name is incorrect.
        """
        config = {"name": "not_a_real_reward_name"}
        with self.assertRaises(LookupError):
            _ = create_reward(config, None)
