"""Unit tests for simulation balance data.
"""
from datetime import datetime

import unittest

from stock_trading_backend.data import SingleValueSimulationData


class TestSingleValueSimulationData(unittest.TestCase):
    """Unit tests for single value simulation data.
    """
    def test_initializes(self):
        """Tests if initializes properly.
        """
        data = SingleValueSimulationData(value_name="balance")
        self.assertEqual("balance", data.id_str)
        self.assertTrue(data.visible)

    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        data = SingleValueSimulationData(value_name="balance")
        data.prepare_data(from_date, to_date, None, None)
        self.assertTrue(data.ready)
        self.assertEqual(32, len(data))

    def test_reset_data(self):
        """Tests if the data is reset properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2020, 1, 1)
        data = SingleValueSimulationData(value_name="balance")
        data.prepare_data(from_date, to_date, None, None)
        self.assertTrue(data.ready)
        data.reset([])
        self.assertFalse(data.ready)
