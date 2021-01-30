"""Class for running a simulation.
"""
import random

import gym

from src.data import create_data_collection


# pylint: disable=too-many-instance-attributes
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
    # pylint: disable=too-many-arguments
    def __init__(self, data_collection_config=None, from_date=None, to_date=None, min_duration=0,
                 max_duration=0, min_start_balance=0, max_start_balance=0, comission=0):
        """Initializer for the simulation class.

        Args:
            data_collection_config: configuration of the data configuration.
            from_date: datetime date for the start of the range
            to_date: datetime date for the end of the range
            min_duration: minimum length of the episode.
            max_duration: maximum length of the episode (if 0 will run for all available dates).
            min_start_balance: minimum starting balance.
            max_start_balance: maximum starting balance. Balance selected unifromly.
            comission: relative comission for each transcation.
        """
        self.data_collection = create_data_collection(data_collection_config)

        self.data_collection.set_date_range(from_date, to_date)
        self.data_collection.prepare_data()
        self.available_dates = self.data_collection.get_available_dates()

        max_duration = min(max_duration, len(self.available_dates))
        self.max_duration = max_duration if max_duration > 0 else len(self.available_dates)
        self.min_duration = min_duration if min_duration > 0 else self.max_duration
        self.min_duration = min(self.max_duration, self.min_duration)

        self.min_start_balance = min_start_balance
        self.max_start_balance = max_start_balance

        self.comission = comission
        self.curr_date = None
        self.episode_end_date = None

    def _prep_for_episode(self):
        """Preparation for the episode.
        """
        self.data_collection.prepare_data()
        duration = random.randint(self.min_duration, self.max_duration)
        curr_date_index = random.randint(0, len(self.available_dates) - duration)
        self.curr_date = self.available_dates[curr_date_index]
        self.episode_end_date = self.available_dates[curr_date_index + duration - 1]
        #return self.data_collection[self.curr_date]

    def step(self, action):
        """Simulate a single day of trading given the action.

        Args:
            action: a list of buy/hold/sell, where ith element shows what to do with ith stock.

        Returns:
            observation: a row of data source.
            reward: a number representing the reward associated with the action.
            done: True if the episode is finished
        """

    def reset(self):
        """Resets the simulation environment.
        """
        self.data_collection.reset()
        return self._prep_for_episode()

    def render(self, mode="human"):
        """Renders current situation.

        Args:
            mode: something
        """
