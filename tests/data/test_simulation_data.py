"""Unit tests for simulation data.
"""
import unittest

from src.data import SimulationData


class TestSimulationData(unittest.TestCase):
    """Unit tests for simulation data.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = SimulationData()

    def test_a(self):
        """A simple test method.
        """
        self.assertTrue(True)
