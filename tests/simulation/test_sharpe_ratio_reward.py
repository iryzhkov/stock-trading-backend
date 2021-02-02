"""Unit tests for Constant Reward class.
"""
from datetime import datetime

import unittest

from stock_trading_backend.simulation.sharpe_ratio_reward import SharpeRatioReward

class TestSharpeRatioReward(unittest.TestCase):
    """Unit test for Sharpe Ratio Reward class.
    """
    def test_initializes(self):
        """Checks if the reward is initialized properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        reward = SharpeRatioReward(from_date, to_date)
        self.assertIsInstance(reward, SharpeRatioReward)

    def test_calculate_value(self):
        """Checks if calculate value works properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        reward = SharpeRatioReward(from_date, to_date)
        date = reward.market_data.index[0]
        reward.reset({"net_worth": 100}, date)
        self.assertEqual(0, reward.calculate_value({"net_worth": 100}, date))
        self.assertEqual(2, reward.calculate_value({"net_worth": 200}, date))

    def test_handles_zero(self):
        """Checks if calculaet value handles zero properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        reward = SharpeRatioReward(from_date, to_date)
        date = reward.market_data.index[0]
        reward.reset({"net_worth": 0}, date)
        self.assertEqual(-1, reward.calculate_value({"net_worth": 0}, date))

    def test_resets(self):
        """Checks if resets properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        reward = SharpeRatioReward(from_date, to_date)
        date = reward.market_data.index[0]
        reward.reset({"net_worth": 100}, date)
        self.assertEqual(1, reward.calculate_value({"net_worth": 200}, date))
        reward.reset({"net_worth": 100}, date)
        self.assertEqual(1, reward.calculate_value({"net_worth": 200}, date))
