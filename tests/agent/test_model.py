"""Unit tests for Model class
"""
import unittest

import pandas as pd
import torch

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
        observation = pd.Series([1, 2, 3], ["balance", "net_worth", "owned"])
        predictions = model.predict(observation, [[0, 1]] * 5)
        self.assertEqual(5, len(predictions))

        def mock_predict(state_action_tensor):
            self.assertIsInstance(state_action_tensor, torch.Tensor)
            self.assertEqual(5, len(state_action_tensor))
        # pylint: disable=protected-access
        model._predict = mock_predict

        _ = model.predict(observation, [[0, 1]] * 5)

    def test_train(self):
        """Checks if train function works properly.
        """
        model = Model()
        def mock_train(state_action_tensor, expected_values_tensor):
            self.assertIsInstance(state_action_tensor, torch.Tensor)
            self.assertIsInstance(expected_values_tensor, torch.Tensor)
            self.assertEqual(5, len(state_action_tensor))
            self.assertEqual(5, len(expected_values_tensor))
        # pylint: disable=protected-access
        model._train = mock_train

        observations = pd.DataFrame([[1, 2, 3]] * 5, columns=["balance", "net_worth", "owned"])
        actions = [1, 0] * 5
        expected_values = [1] * 5
        model.train(observations, actions, expected_values)
