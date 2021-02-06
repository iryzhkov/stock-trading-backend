"""Unit tests for backtesting.
"""
from datetime import datetime

import unittest

from parameterized import parameterized

from stock_trading_backend import api
from stock_trading_backend.backtest import backtest_agent


class TestBacktest(unittest.TestCase):
    """Unit tests for backtesting.
    """
    def is_output_valid(self, output):
        """Checks if the backtesting output is valid.

        Args:
            output: output dict to check.
        """
        self.assertIn("overall_reward", output)
        self.assertIn("stock_names", output)
        self.assertIn("net_worth_history", output)
        self.assertIn("balance_history", output)
        self.assertIn("owned_stocks_history", output)
        self.assertIn("action_history", output)
        self.assertIn("stocks_price_history", output)
        self.assertEqual(len(output["net_worth_history"]), len(output["balance_history"]))
        self.assertEqual(len(output["owned_stocks_history"]), len(output["balance_history"]))
        self.assertEqual(len(output["stocks_price_history"]), len(output["balance_history"]))
        self.assertEqual(len(output["action_history"]) + 1, len(output["balance_history"]))
        self.assertEqual(len(output["reward_history"]) + 1, len(output["balance_history"]))

    @parameterized.expand([
        ("following_feature_agent_1", "default"),
        ("following_feature_agent_1", "real_stock_1"),
    ])
    def test_backtest(self, agent_name, data_collection_name):
        """Checks if backtesting works.

        Args:
            agent_name: the agent to test backtesting with.
            data_collection_name: the data collection to test backtesting with.
        """
        agent = api.get_agent_object(agent_name, data_collection_name)
        output = backtest_agent(agent, from_date=datetime(2015, 2, 1),
                                to_date=datetime(2015, 3, 1))
        self.is_output_valid(output)

    def test_backtest_with_kwargs(self):
        """Checks if backtesting works for agents that produce kwargs.
        """
        agent = api.get_agent_object("sarsa_learning_agent_1", model_name="linear")
        agent.trained = True
        output = backtest_agent(agent)
        self.is_output_valid(output)
        self.assertIn("sa_value", output)

    def test_not_usable_agent(self):
        """Checks if non-usable agents raise error with backtest.
        """
        with self.assertRaises(ValueError):
            agent = api.get_agent_object("sarsa_learning_agent_1", model_name="linear")
            backtest_agent(agent)

    def test_multiple_backtests(self):
        """Checks if can run the backtest multiple times on an agent.
        """
        agent = api.get_agent_object()
        output = backtest_agent(agent)
        self.is_output_valid(output)
        output = backtest_agent(agent)
        self.is_output_valid(output)
