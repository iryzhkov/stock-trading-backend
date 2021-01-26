"""Unit tests for stock market simulation.
"""
import unittest

from src.simulation import Simulation


class TestGeneratedStockData(unittest.TestCase):
    """Unit tests for generated stock data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.simulation = Simulation()

    def test_a(self):
        """A simple test method.
        """
        self.assertTrue(True)
