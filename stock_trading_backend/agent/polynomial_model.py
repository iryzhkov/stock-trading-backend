"""Polynomial model class used by agents for building stuff.
"""
from stock_trading_backend.agent.model import Model


class PolynomialModel(Model):
    """Polynomial model class.
    """
    name = "polynomial"

    def __init__(self, degree=1):
        """Initializer for model class.

        Args:
            degree: the maximum degree of polynomial. (1 is linear, 2 is quadratic, etc.,).
        """
        super(PolynomialModel, self).__init__()
        self.degree = degree
        self.id_str = "{}_{}".format(self.name, degree)

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
