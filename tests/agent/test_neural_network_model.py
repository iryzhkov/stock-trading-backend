"""Unit tests for Neural Network Model class
"""
import unittest

import pandas as pd

from stock_trading_backend.agent import NeuralNetworkModel


class TestNeuralNetworkModel(unittest.TestCase):
    """Unit tests for Neural Network Model class.
    """
    def test_initializes(self):
        """Checks if model initializes properly.
        """
        model = NeuralNetworkModel(learning_rate=1)
        self.assertEqual(1, model.learning_rate)

    def test_predict(self):
        """Checks if predict function works properly.
        """
        model = NeuralNetworkModel()
        observation = pd.Series([1, 2, 3], ["balance", "net_worth", "owned"])
        predictions = model.predict(observation, [[0, 1]] * 5)
        self.assertEqual(5, len(predictions))

    def test_train(self):
        """Checks if train function works properly.
        """
        model = NeuralNetworkModel()
        observations = pd.DataFrame([[1, 2, 3]] * 10, columns=["balance", "net_worth", "owned"])
        actions = [[0]] * 5 + [[1]] * 5
        expected_values = [[0]] * 5 + [[1]] * 5
        losses = [model.train(observations, actions, expected_values) for i in range(10)]
        self.assertTrue(losses[0] > losses[-1])
