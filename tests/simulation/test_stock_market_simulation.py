"""Unit tests for stock market simulation.
"""
import unittest

from src.simulation import StockMarketSimulation


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.simulation = StockMarketSimulation(None)

    def test_a(self):
        """A simple test method.
        """
        self.assertIsNone(self.simulation.data_source_config)
