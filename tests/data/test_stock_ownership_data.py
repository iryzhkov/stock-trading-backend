"""Unit tests for simulation stock ownership data.
"""
import unittest

from src.data import StockOwnershipData


class TestStockOwnershipData(unittest.TestCase):
    """Unit tests for simulation stock ownership data.
    """
    def test_prepare_data(self):
        """Tests if the data is prepared properly.
        """
        data = StockOwnershipData()
        data.prepare_data(None, None, None, None)
        self.assertFalse(data.ready)
