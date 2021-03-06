"""Unit tests for data.
"""
import unittest

import pandas as pd

from stock_trading_backend.data import Data


class TestData(unittest.TestCase):
    """Unit tests for data.
    """
    def test_checks_num_dependencies(self):
        """Test for number of dependencies check.
        """
        with self.assertRaises(ValueError):
            Data(dependencies=["stock_data"])
        Data()

    def test_len(self):
        """Test __len__ function.
        """
        expected_length = 25
        data = Data()
        data.data = [0] * expected_length
        self.assertEqual(expected_length, len(data))

    def test_iter(self):
        """Tests __iter__ function.
        """
        arr = list(range(25))
        data = Data()
        data.data = arr
        for expected_value, value in zip(arr, data):
            self.assertEqual(expected_value, value)

    def test_contains(self):
        """Tests __contains__ function.
        """
        data = Data()
        data.data = pd.DataFrame(data=[True] * 5)
        for i in range(5):
            self.assertIn(i, data)
        for i in range(5, 10):
            self.assertNotIn(i, data)

    def test_get(self):
        """Tests __getitem__ function.
        """
        data = Data()
        data.data = pd.DataFrame(data=[True] * 5)
        for i in range(5):
            self.assertEqual(True, data[i].item())

        with self.assertRaises(LookupError):
            _ = data[6]

    def test_hash(self):
        """Tests __hash__ function.
        """
        data = Data()
        self.assertIsNotNone(hash(data))

    def test_setitem(self):
        """Tests if the data can be set properly.
        """
        data = Data()
        data.data = pd.DataFrame(data=[True] * 5)
        data[0] = False
        self.assertFalse(data[0].item())

    def test_buffer_days(self):
        """Tests buffer_days function.
        """
        data = Data()
        data.buffer_days([])
        self.assertEqual(0, data.buffer)
        data.buffer_days([0, 10])
        self.assertEqual(10, data.buffer)
