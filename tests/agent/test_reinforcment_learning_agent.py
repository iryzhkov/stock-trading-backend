"""Unit tests for reinforcement learning agent.
"""
from stock_trading_backend.agent import ReinforcementLearningAgent

from tests.agent.test_with_simulation import TestWithSimulation


class TestReinforcementLearningAgent(TestWithSimulation):
    """Unit tests for reinforcement learning agent.
    """
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        agent = ReinforcementLearningAgent(self.data_collection_config, None)
        self.assertEqual(self.data_collection_config, agent.data_collection_config)
