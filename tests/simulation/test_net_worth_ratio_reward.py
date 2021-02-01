"""Unit tests for Constant Reward class.
"""
import unittest

from stock_trading_backend.simulation.net_worth_ratio_reward import NetWorthRatioReward

class TestNetWorthRatioReward(unittest.TestCase):
    """Unit test for Net Worth Ratio Reward class.
    """
    def test_initializes(self):
        """Checks if the reward is initialized properly.
        """
        reward = NetWorthRatioReward()
        self.assertIsInstance(reward, NetWorthRatioReward)

    def test_calculate_value(self):
        """Checks if calculate value works properly.
        """
        reward = NetWorthRatioReward()
        reward.reset({"net_worth": 100}, None)
        self.assertEqual(0, reward.calculate_value({"net_worth": 100}, None))
        self.assertEqual(1, reward.calculate_value({"net_worth": 200}, None))

    def test_handles_zero(self):
        """Checks if calculaet value handles zero properly.
        """
        reward = NetWorthRatioReward()
        reward.reset({"net_worth": 100}, None)
        self.assertEqual(-1, reward.calculate_value({"net_worth": 0}, None))
        self.assertEqual(-1, reward.calculate_value({"net_worth": 0}, None))

    def test_resets(self):
        """Checks if resets properly.
        """
        reward = NetWorthRatioReward()
        reward.reset({"net_worth": 100}, None)
        self.assertEqual(1, reward.calculate_value({"net_worth": 200}, None))
        reward.reset({"net_worth": 100}, None)
        self.assertEqual(1, reward.calculate_value({"net_worth": 200}, None))