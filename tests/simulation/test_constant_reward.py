"""Unit tests for Constant Reward class.
"""
import unittest

from stock_trading_backend.simulation.constant_reward import ConstantReward

class TestConstantReward(unittest.TestCase):
    """Unit test for Constant Reward class.
    """
    def test_initializes(self):
        """Checks if the reward is initialized properly.
        """
        reward = ConstantReward()
        self.assertIsInstance(reward, ConstantReward)
        self.assertEqual(0, reward.calculate_value(None, None))

        reward = ConstantReward(5)
        self.assertEqual(5, reward.calculate_value(None, None))

    def test_resets(self):
        """Checks if Constant Reward resets properly.
        """
        reward = ConstantReward()
        reward.reset(None, None)
        reward.calculate_value(None, None)
        self.assertEqual(0, reward.calculate_value(None, None))
