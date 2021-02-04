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
        reward = backtest_agent(agent)
        self.assertTrue(reward > -0.5)

    def test_multiple_backtests(self):
        """Checks if can run the backtest multiple times on an agent.
        """
        agent = api.get_agent_object()
        reward = backtest_agent(agent)
        self.assertTrue(reward > -0.5)
        reward = backtest_agent(agent)
        self.assertTrue(reward > -0.5)

    def test_long_backtest(self):
        """Check how backtesting works for 2-year simulation.
        """
        agent = api.get_agent_object("following_feature_agent_1", "real_stock_2", "net_worth_ratio")
        reward = backtest_agent(agent, from_date=datetime(2014, 1, 1), to_date=datetime(2016, 1, 1))
        self.assertTrue(reward > 0)
