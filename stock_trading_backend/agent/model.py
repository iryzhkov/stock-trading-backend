"""Base model class used by agents for building stuff.
"""
from abc import ABCMeta

import numpy as np
import pandas as pd
import torch
# pylint: disable=no-member
torch.set_default_dtype(torch.float64)


class Model(metaclass=ABCMeta):
    """Base model class.
    """
    name = None

    def __init__(self):
        """Initializer for model class.
        """
        self.id_str = self.name

    # pylint: disable=no-self-use
    def _predict(self, state_action_tensor):
        """Use provided information to make a prediction.

        Args:
            state_action_tensor: pytorch tensor with state-action values.

        Returns:
            Predicted values for observation-action tensors.
        """
        return [0] * len(state_action_tensor)

    def predict(self, observation, actions):
        """Converts observation and actions into tensor and passes them to _predict function.

        Args:
            observation: state of the simulation
            actions: list of actions (each action can be used as: simulation.step(action)).

        Returns:
            Predicted values for observation-action pairs.
        """
        action_df = pd.DataFrame(actions)
        observation_df = pd.DataFrame([observation] * len(actions), columns=observation.index,
                                      index=action_df.index)
        state_action_df = observation_df.merge(action_df, left_index=True, right_index=True)
        # pylint: disable=no-member
        # pylint: disable=not-callable
        state_action_tensor = torch.tensor(state_action_df.values, dtype=torch.float64)
        return self._predict(state_action_tensor)

    def predict_with_multiple_observations(self, observations, actions):
        """Use provided information to make a prediction.

        Args:
            state_action_tensor: pytorch tensor with state-action expected_values.
            expected_values: pytorch tensor with expected values for each state-action.

        Returns:
            Predicted values for observation-action tensors.
        """
        action_df = pd.DataFrame(actions)
        observation_df = pd.DataFrame(observations)
        state_action_df = observation_df.merge(action_df, left_index=True, right_index=True)
        # pylint: disable=no-member
        # pylint: disable=not-callable
        state_action_tensor = torch.tensor(state_action_df.values, dtype=torch.float64)
        return self._predict(state_action_tensor)

    # pylint: disable=no-self-use
    def _train(self, state_action_tensor, expected_values_tensor):
        """Train the model for 1 epoch.

        Args:
            state_action_tensor: pytorch tensor with state-action expected_values.
            expected_values: pytorch tensor with expected values for each state-action.

        Returns:
            The loss before trainig.
        """

    def train(self, observations, actions, expected_values):
        """Convert observations and actions into tensor and pass them to _train.

        Args:
            observations: a dataframe of simulation states.
            actions: a list of actions.
            expected_values: a list of expected values for each observation-action pair.

        Returns:
            The loss before trainig.
        """
        action_df = pd.DataFrame(actions)
        observation_df = pd.DataFrame(observations)
        state_action_df = observation_df.merge(action_df, left_index=True, right_index=True)
        # pylint: disable=not-callable
        state_action_tensor = torch.tensor(state_action_df.values.astype(np.float64, copy=False))
        # pylint: disable=no-member
        # pylint: disable=not-callable
        expected_values_tensor = torch.tensor(expected_values, dtype=torch.float64).reshape(-1, 1)
        return self._train(state_action_tensor, expected_values_tensor)
