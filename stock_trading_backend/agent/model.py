"""Base model class used by agents for building stuff.
"""
from abc import ABCMeta


class Model(metaclass=ABCMeta):
    """Base model class.
    """
    name = None

    def __init__(self):
        """Initializer for model class.
        """
        self.id_str = self.name

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    def predict(self, observation, actions):
        """Use provided information to make a prediction.

        Args:
            observation: state of the simulation
            actions: list of actions (each action can be used as: simulation.step(action)).

        Returns:
            Predicted values for observation-action pairs.
        """
        return [0] * len(actions)

    # pylint: disable=unused-argument
    def train(self, observations, actions, expected_values):
        """Train on the provided information for 1 epoch.

        Args:
            observations: a list of simulation states.
            actions: a list of actions.
            expected_values: a list of expected values for each observation-action pair.
        """
