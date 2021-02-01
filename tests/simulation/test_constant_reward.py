"""Unit tests for Constant Reward class.
"""
import unittest

from stock_trading_backend.simulation.constant_reward import ConstantReward

class TestConstantReward(unittest.TestCase):
    """Unit test for Reard class.
    """
    def test_initializes(self):
        """Checks if the reward is initialized properly.
        """
        reward = ConstantReward(None)
        self.assertIsInstance(reward, ConstantReward)
        self.assertEqual(0, reward.value)

        reward = ConstantReward(None, 5)
        self.assertEqual(5, reward.value)

    def test_calculate_value(self):
        """Checks if calculate_value works properly.
        """
        reward = ConstantReward(None)
        reward.calculate_value(None)
        self.assertEqual(0, reward.value)

    def test_resets(self):
        """Checks if Constant Reward resets properly.
        """
        reward = ConstantReward(None)
        reward.reset()
        reward.calculate_value(None)
        self.assertEqual(0, reward.value)
