"""Unit tests for Model class
"""
import unittest

from stock_trading_backend.agent import Model


class TestModel(unittest.TestCase):
    """Unit tests for Model class.
    """
    def test_initializes(self):
        """Checks if model initializes properly.
        """
        model = Model()
        self.assertIsNone(model.name)

    def test_predict(self):
        """Checks if predict function works properly.
        """
        model = Model()
        predictions = model.predict(None, [0] * 5)
        self.assertEqual(5, len(predictions))
        self.assertEqual(0, predictions[0])
