"""Base class for reward.
"""
from abc import ABCMeta


class Reward(metaclass=ABCMeta):
    """Base class for reward.
    """
    name = None

    # pylint: disable=unused-argument
    def __init__(self, env=None):
        """Initializer for reward class.

        Args:
            env: StockMarketSimulation enviroment for which the Reward is build.
        """

    def calculate_value(self, observation):
        """Calculates the value of the reward given the observation.

        Args:
            observation: observation from the environemnt.
        """

    def reset(self):
        """Resets the internal reward state.
        """
