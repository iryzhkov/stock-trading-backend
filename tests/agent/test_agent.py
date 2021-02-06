"""Unit tests for agent.
"""
from stock_trading_backend.agent import Agent

from tests.agent.test_with_simulation import TestWithSimulation


class TestAgent(TestWithSimulation):
    """Unit tests for agent.
    """
    def test_initializes(self):
        """A test to see if agent is initialized properly.
        """
        agent = Agent(self.data_collection_config, None)
        self.assertEqual(self.data_collection_config, agent.data_collection_config)
        self.assertTrue(agent.usable)

    def test_observation_unpack(self):
        """A test to see if observation unpack works.
        """
        agent = Agent(self.data_collection_config, None)
        observation = self.simulation.reset()
        balance, net_worth, owned_stocks, stock_prices = agent.unpack_observation(observation)
        self.assertEqual(100, balance)
        self.assertEqual(100, net_worth)
        self.assertTrue(([0, 0] == owned_stocks))
        self.assertTrue(([20, 10] == stock_prices))

        observation, _, _ = self.simulation.step([1, 1])
        balance, net_worth, owned_stocks, stock_prices = agent.unpack_observation(observation)
        self.assertEqual(10, balance)
        self.assertEqual(100, net_worth)
        self.assertTrue(([1, 1] == owned_stocks))
        self.assertTrue(([20, 10] == stock_prices))

    def test_make_decision(self):
        """A test to see if agent can make decisions.
        """
        agent = Agent(self.data_collection_config, None)
        observation = self.simulation.reset()

        while not self.simulation.done:
            action, _ = agent.make_decision(observation, self.simulation)
            self.assertEqual(2, len(action))
            observation, _, _ = self.simulation.step(action)
            _, net_worth, _, _ = agent.unpack_observation(observation)
            self.assertEqual(100, net_worth)
