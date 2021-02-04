"""Class for net worth growth ratio reward.
"""
from stock_trading_backend.simulation.reward import Reward


class NetWorthRatioReward(Reward):
    """Net worth growth ratio reward class.
    """
    name = "net_worth_ratio_reward"

    # pylint: disable=unused-argument
    def __init__(self, from_date=None, to_date=None):
        """Initializer for reward class.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
        """
        super(NetWorthRatioReward, self).__init__(from_date, to_date)
        self.prev_net_worth = 0
        self.first_net_worth = 0
        self.num_days = 0

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
        self.num_days += 1
        return result

    def calculate_overall_reward(self):
        """Calculates the value of the reward for the whole episode.
        """
        return ((self.prev_net_worth / self.first_net_worth)  - 1) / self.num_days

    # pylint: disable=unused-argument
    def reset(self, observation, date):
        """Resets the internal reward state.

        Args:
            observation: state of the reset environment.
            date: datetime current date in the environment
        """
        self.prev_net_worth = observation["net_worth"]
        self.first_net_worth = observation["net_worth"]
        self.num_days = 0
