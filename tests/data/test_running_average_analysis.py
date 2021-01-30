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
        self.assertTrue(data.ready)

    def test_resets_data(self):
        """Tests if the data is reset properly.
        """
        data = RunningAverageAnalysis(dependencies=["stock_data"])
        data.prepare_data(None, None, None, None)
        self.assertTrue(data.ready)
        data.reset([True])
        self.assertTrue(data.ready)

    def test_buffer_days(self):
        """Tests if number of buffer days is calculated.
        """
        data = RunningAverageAnalysis(dependencies=["stock_data"], num_days=30)
        data.buffer_days([0])
        self.assertEqual(30, data.buffer)
