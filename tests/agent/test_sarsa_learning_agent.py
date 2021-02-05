"""Unit tests for sarsa learning agent.
"""
import unittest

import pandas as pd

from stock_trading_backend.agent import SARSALearningAgent
from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file


class TestSarsaLearningAgent(unittest.TestCase):
    """Unit tests for sarsa learning agent.
    """
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        model_config = read_config_file("model/linear.yaml")
        agent = SARSALearningAgent(data_collection_config=data_collection_config,
                                   model_config=model_config)
        self.assertEqual(data_collection_config, agent.data_collection_config)
        self.assertFalse(agent.usable)

    def test_without_model_errer(self):
        """Checks if the agent raises error when initialized without model config.
        """
        with self.assertRaises(ValueError):
            data_collection_config = read_config_file("test/simulation.yaml")
            _ = SARSALearningAgent(data_collection_config=data_collection_config)

    def test_apply_learning(self):
        """A test to see if sarsa agent can apply learning.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        model_config = read_config_file("model/linear.yaml")
        agent = SARSALearningAgent(data_collection_config=data_collection_config,
                                   model_config=model_config, discount_factor=0.5)

        observations = pd.DataFrame([[0]] * 6, columns=["balance"])
        actions = [[0]] * 3 + [[1]] * 3
        rewards = [[0]] * 3 + [[1]] * 3

        # Testing whther sarsa learning agent changes trained variable.
        agent.apply_learning(observations, actions, rewards)
        self.assertTrue(agent.usable)

        # pylint: disable=unused-variable
        for i in range(5):
            agent.apply_learning(observations, actions, rewards)

    def test_make_decision(self):
        """A test to see if agent can make decisions.
        """
        data_collection_config = read_config_file("test/simulation.yaml")
        model_config = read_config_file("model/linear.yaml")
        agent = SARSALearningAgent(data_collection_config=data_collection_config,
                                   model_config=model_config)
        simulation = StockMarketSimulation(data_collection_config)
        observation = simulation.reset()

        # Testing whether sarsa learning agent makes a valid decision.
        action = agent.make_decision(observation, simulation)
        self.assertEqual(2, len(action))
