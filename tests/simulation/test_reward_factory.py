"""Unit tests for reward factory.
"""
from datetime import datetime

import unittest

from parameterized import parameterized

from stock_trading_backend.simulation import create_reward
from stock_trading_backend.simulation.constant_reward import ConstantReward
from stock_trading_backend.simulation.net_worth_ratio_reward import NetWorthRatioReward
from stock_trading_backend.simulation.sharpe_ratio_reward import SharpeRatioReward

class TestRewardFactory(unittest.TestCase):
    """Tests for reward factory.
    """
    @parameterized.expand([
        ({"name": "constant"}, ConstantReward),
        ({"name": "net_worth_ratio"}, NetWorthRatioReward),
        ({"name": "sharpe_ratio"}, SharpeRatioReward),
    ])
    def test_creates_correct_class(self, reward_config, expected_class):
        """Tests if creat_reward creates the correct class.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        reward = create_reward(reward_config, from_date, to_date)
        self.assertIsInstance(reward, expected_class)

    def test_raises_lookup_error(self):
        """Tests if creat_reward raises lookup error when name is incorrect.
        """
        config = {"name": "not_a_real_reward_name"}
        with self.assertRaises(LookupError):
            _ = create_reward(config, None, None)
