"""Unit tests for reinforcement learning agent.
"""
import unittest

from stock_trading_backend.agent import ReinforcementLearningAgent


class TestReinforcementLearningAgent(unittest.TestCase):
    """Unit tests for reinforcement learning agent.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.agent = ReinforcementLearningAgent(None, None)

    def test_a(self):
        """A simple test method.
        """
        self.assertFalse(self.agent.data_source_config)
