"""Unit tests for simulation balance data.
"""
import unittest

from src.data import BalanceData


class TestBalanceData(unittest.TestCase):
    """Unit tests for simulation balance data.
    """
    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        data = BalanceData()
        data.prepare_data(None, None, None, None)
        self.assertFalse(data.ready)
