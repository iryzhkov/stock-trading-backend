"""Base test class with set up simulation.
"""
from datetime import datetime

import unittest

from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file


class TestWithSimulation(unittest.TestCase):
    """Unit tests for agent.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 1, 5)
        self.data_collection_config = read_config_file("test/simulation.yaml")
        self.simulation = StockMarketSimulation(self.data_collection_config, from_date, to_date,
                                                min_start_balance=100, max_start_balance=100,
                                                max_stock_owned=2)
