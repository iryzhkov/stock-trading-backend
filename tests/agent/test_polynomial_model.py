"""Unit tests for PolynomialModel class
"""
import unittest

import pandas as pd

from stock_trading_backend.agent import PolynomialModel


class TestPolynomialModel(unittest.TestCase):
    """Unit tests for PolynomialModel class.
    """
    def test_initializes(self):
        """Checks if model initializes properly.
        """
        model = PolynomialModel(degree=5)
        self.assertEqual(5, model.degree)
        with self.assertRaises(ValueError):
            _ = PolynomialModel(degree=0)

    def test_predict(self):
        """Checks if predict function works properly.
        """
        model = PolynomialModel()
        observation = pd.Series([1, 2, 3], ["balance", "net_worth", "owned"])
        predictions = model.predict(observation, [[0, 1]] * 5)
        print(predictions)
        self.assertEqual(5, len(predictions))

    def test_train(self):
        """Checks if train function works properly.
        """
        model = PolynomialModel(degree=2)
        observations = pd.DataFrame([[1, 2, 3]] * 10, columns=["balance", "net_worth", "owned"])
        actions = [[0]] * 5 + [[1]] * 5
        expected_values = [[0]] * 5 + [[1]] * 5
        losses = [model.train(observations, actions, expected_values) for i in range(10)]
        self.assertTrue(losses[0] > losses[-1])
