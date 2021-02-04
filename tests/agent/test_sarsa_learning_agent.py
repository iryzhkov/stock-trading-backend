"""Unit tests for sarsa learning agent.
"""
import unittest

from stock_trading_backend.agent import SARSALearningAgent
from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file

class TestLearningAgent(unittest.TestCase):
    """Unit tests for q learning agent.
    """
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        agent = SARSALearningAgent(data_collection_config, None)
        self.assertEqual(data_collection_config, agent.data_collection_config)
        self.assertFalse(agent.usable)

    def test_make_decision(self):
        """A test to see if agent can make decisions.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        agent = SARSALearningAgent(data_collection_config, None)
        simulation = StockMarketSimulation(data_collection_config)
        observation = simulation.reset()
        action = agent.make_decision(observation, simulation)
        self.assertEqual(2, len(action))

    def test_apply_learning(self):
        """A test to see if agent can apply learning.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        agent = SARSALearningAgent(data_collection_config, None)
        agent.apply_learning()
        self.assertTrue(agent.usable)
