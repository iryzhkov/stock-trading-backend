"""Unit tests for agent.
"""
import unittest

import pandas as pd

from stock_trading_backend.agent import QLearningAgent
from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file


class TestQLearningAgent(unittest.TestCase):
    """Unit tests for q learning agent.
    """
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        agent = QLearningAgent(data_collection_config, None)
        self.assertEqual(data_collection_config, agent.data_collection_config)
        self.assertFalse(agent.usable)

    def test_make_decision(self):
        """A test to see if agent can make decisions.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        agent = QLearningAgent(data_collection_config, None)
        simulation = StockMarketSimulation(data_collection_config, reward_config=None)
        observation = simulation.reset()

        # Testing whether q learning makes a valid decision.
        action = agent.make_decision(observation, simulation)
        self.assertEqual(2, len(action))

    def test_apply_learning(self):
        """A test to see if q learning agent can apply learning.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        agent = QLearningAgent(data_collection_config, None)

        observations = pd.DataFrame([[1]] * 6, columns=["shmalance"])
        actions = [[0]] * 3 + [[1]] * 3
        rewards = [-1] * 3 + [1] * 3

        # Testing whther q learning agent changes trained variable.
        agent.apply_learning(observations, actions, rewards)
        self.assertTrue(agent.usable)
