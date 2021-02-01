"""Unit tests for agent.
"""
import unittest

from stock_trading_backend.agent import Agent


class TestAgent(unittest.TestCase):
    """Unit tests for agent.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.agent = Agent(None)

    def test_a(self):
        """A simple test method.
        """
        self.assertFalse(self.agent.data_source_config)
