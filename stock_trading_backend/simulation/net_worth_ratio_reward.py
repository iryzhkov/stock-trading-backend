"""Class for net worth growth ratio reward.
"""
from stock_trading_backend.simulation.reward import Reward


class NetWorthRatioReward(Reward):
    """Net worth growth ratio reward class.
    """
    name = "net_worth_ratio"

    def __init__(self):
        """Initializer for reward class.
        """
        self.prev_net_worth = 0

    # pylint: disable=unused-argument
    def calculate_value(self, observation, date):
        """Calculates the value of the reward given the observation.

        Args:
            observation: observation from the environemnt.
            date: datetime current date in the environment
        """
        if self.prev_net_worth <= 0:
            return -1
        curr_net_worth = observation["net_worth"]
        result = (curr_net_worth / self.prev_net_worth) - 1
        self.prev_net_worth = curr_net_worth
        return result

    # pylint: disable=unused-argument
    def reset(self, observation, date):
        """Resets the internal reward state.

        Args:
            observation: state of the reset environment.
            date: datetime current date in the environment
        """
        self.prev_net_worth = observation["net_worth"]
