"""Class for net worth growth ratio reward.
"""
import numpy as np

from stock_trading_backend.simulation.reward import Reward
from stock_trading_backend.util import get_stock_data


class SharpeRatioReward(Reward):
    """Sharpe ratio reward class.
    """
    name = "sharpe_ratio_reward"

    def __init__(self, from_date=None, to_date=None):
        """Initializer for reward class.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
        """
        super(SharpeRatioReward, self).__init__(from_date, to_date)
        self.first_net_worth = 0
        self.prev_net_worth = 0
        self.first_market_value = 0
        self.prev_market_value = 0
        self.returns = []
        self.market_returns = []
        self.market_data = get_stock_data(["SPY"], from_date, to_date)

    def calculate_value(self, observation, date):
        """Calculates the value of the reward given the observation.

        Args:
            observation: observation from the environemnt.
            date: datetime current date in the environment
        """
        if self.prev_net_worth == 0:
            return -1

        curr_net_worth = observation["net_worth"]
        curr_market_value = self.market_data.loc[date].item()

        curr_return = curr_net_worth / self.prev_net_worth - 1
        market_return = curr_market_value / self.prev_market_value - 1
        self.returns.append(curr_return)
        self.market_returns.append(market_return)

        result = np.mean(self.returns) - np.mean(self.market_returns)
        if len(self.returns) > 1:
            result /= np.std(self.returns)

        self.prev_net_worth = curr_net_worth
        self.prev_market_value = curr_market_value
        return result

    def calculate_overall_reward(self):
        """Calculates the value of the reward for the whole episode.
        """
        agent_return = self.prev_net_worth / self.first_net_worth - 1
        market_return = self.prev_market_value / self.first_market_value - 1

        result = (agent_return - market_return) / len(self.returns)
        if len(self.returns) > 1:
            result /= np.std(self.returns)

        return result

    def reset(self, observation, date):
        """Resets the internal reward state.

        Args:
            observation: state of the reset environment.
            date: datetime current date in the environment
        """
        self.prev_net_worth = observation["net_worth"]
        self.prev_market_value = self.market_data.loc[date].item()
        self.first_net_worth = self.prev_net_worth
        self.first_market_value = self.prev_market_value
        self.returns = []
        self.market_returns = []
