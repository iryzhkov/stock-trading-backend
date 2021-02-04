"""Unit tests for PolynomialModel class
"""
import unittest

from stock_trading_backend.agent import PolynomialModel


class TestPolynomialModel(unittest.TestCase):
    """Unit tests for PolynomialModel class.
    """
    def test_initializes(self):
        """Checks if model initializes properly.
        """
        model = PolynomialModel(degree=5)
        self.assertEqual(5, model.degree)

    def test_predict(self):
        """Checks if predict function works properly.
        """
        model = PolynomialModel()
        predictions = model.predict(None, [0] * 5)
        self.assertEqual(5, len(predictions))
        self.assertEqual(0, predictions[0])
