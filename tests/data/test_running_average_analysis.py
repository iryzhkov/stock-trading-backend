"""Unit tests for running average analysis.
"""
import unittest

from src.data import RunningAverageAnalysis


class TestRunningAverageAnalysis(unittest.TestCase):
    """Unit tests for running average analysis.
    """
    def test_id_str(self):
        """Tests if the id_str is correct.
        """
        data = RunningAverageAnalysis(dependencies=["stock_data"])
        self.assertEqual("running_average_1_for_stock_data", data.id_str)

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        data = RunningAverageAnalysis(dependencies=["stock_data"])
        data.prepare_data(None, None, None, None)
