"""Base class for reward.
"""
from abc import ABCMeta


class Reward(metaclass=ABCMeta):
    """Base class for reward.
    """
    name = None

    def __init__(self, from_date=None, to_date=None):
        """Initializer for base class.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
        """
        self.id_str = self.name

    def calculate_value(self, observation, date):
        """Calculates the value of the reward given the observation.

        Args:
            observation: observation from the environemnt.
            date: datetime current date in the environment
        """

    def calculate_overall_reward(self):
        """Calculates the value of the reward for the whole episode.
        """

    def __hash__(self):
        """Returns hash of self.id_str
        """
        return hash(self.id_str)

    def reset(self, observation, date):
        """Resets the internal reward state.

        Args:
            observation: state of the reset environment.
            date: datetime current date in the environment
        """
