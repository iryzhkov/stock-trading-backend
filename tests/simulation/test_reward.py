"""Unit tests for Reward class.
"""
import unittest

from stock_trading_backend.simulation.reward import Reward

class TestReward(unittest.TestCase):
    """Unit test for Reard class.
    """
    def test_initializes(self):
        """Checks if the reward is initialized properly.
        """
        reward = Reward(None)
        self.assertIsInstance(reward, Reward)
        self.assertEqual(0, reward.value)

        reward = Reward(None, 5)
        self.assertEqual(5, reward.value)

    def test_calculate_value(self):
        """Checks if calculate_value works properly.
        """
        reward = Reward(None)
        reward.calculate_value(None)
        self.assertEqual(0, reward.value)

    def test_resets(self):
        """Checks if Reward resets properly.
        """
        reward = Reward(None)
        reward.reset()
        reward.calculate_value(None)
        self.assertEqual(0, reward.value)
