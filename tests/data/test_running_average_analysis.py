"""Unit tests for running average analysis.
"""
import unittest

from src.data import RunningAverageAnalysis


class TestRunningAverageAnalysis(unittest.TestCase):
    """Unit tests for running average analysis.
    """
    def setUp(self):
        """Set up for the unit tests.
        """
        self.data = RunningAverageAnalysis(["real_stock_data"])

    def test_a(self):
        """A simple test method.
        """
        self.assertFalse(self.data.data)
