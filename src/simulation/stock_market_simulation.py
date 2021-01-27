"""Class for running a simulation.
"""
import gym

class StockMarketSimulation(gym.Env):
    """
    Description:
        A simulation of the stock market.

    Observation:
        TODO(igor.o.ryzhkov@gmail.com): add description.

    Actions:
        TODO(igor.o.ryzhkov@gmail.com): add description.

    Reward:
        TODO(igor.o.ryzhkov@gmail.com): add description.

    Starting State:
        Agent starts with 0 stocks. The amount of money is selected uniformly in the given range.
        The date is selected uniformly in the date range. The length of the simulation is selected
        uniformly in the length range.

    Episode Termination:
        Episode length is greater than allowed.
    """
    def __init__(self, data_source_config):
        """Initializer for the simulation class.

        Args:
            data_source_config: configuration of the data source.
        """
        self.data_source_config = data_source_config

    def step(self, action):
        """Simulate a single day of trading given the action.

        Args:
            action: a list of buy/hold/sell, where ith element shows what to do with ith stock.

        Returns:
            observation: a row of data source.
            reward: a number representing the reward for the day.
            done: True if the simulation is finished
        """

    def reset(self):
        """Resents the simulation environment.
        """

    def render(self, mode="human"):
        """Renders current situation.

        Args:
            mode: something
        """
