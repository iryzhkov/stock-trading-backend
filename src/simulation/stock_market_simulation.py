"""Class for running a simulation.
"""
from datetime import timedelta

import random
import math

import gym
import numpy as np

from src.data import create_data_collection, SingleValueSimulationData, StockOwnershipData


# pylint: disable=too-many-instance-attributes
class StockMarketSimulation(gym.Env):
    """
    Description:
        A simulation of the stock market.

    Observation:
        Observation space is mostly determined in the data collection config. All observation spaces
        contain stock price data, balance data, net worth data, stocks owned data. Additional
        features, such as running average, deriviative, date metadata, etc., can be used in this
        environment.

    Actions:
        Type: MultiBinary(len(stock_names))
        Num Action
        0   Hold. Does not do anything with the ith stock.
        1   Buy/Sell. If stock is owned, then sell, if not, then buy.

        Note: Sell action is not always executed. When there is not enough balance, the first stocks
        are bought first, the last sell orders are ignored if not enough balance.

        Note: The simulation spends about 1 / max_stock_owned of the net-worth on each stock
        purchase.

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
    def __init__(self, data_collection_config, from_date, to_date, min_duration=0,
                 max_duration=0, min_start_balance=0, max_start_balance=0, commission=0,
                 max_stock_owned=1):
        """Initializer for the simulation class.

        Args:
            data_collection_config: configuration of the data configuration.
            from_date: datetime date for the start of the range
            to_date: datetime date for the end of the range
            min_duration: minimum length of the episode.
            max_duration: maximum length of the episode (if 0 will run for all available dates).
            min_start_balance: minimum starting balance.
            max_start_balance: maximum starting balance. Balance selected unifromly.
            commission: relative commission for each transcation.
            max_stock_owned: a maximum number of different stocks that can be owned.
        """
        self.data_collection = create_data_collection(data_collection_config)

        # Setup of simulation data.
        self.stock_data = self.data_collection.data_objects[0]
        self.balance = SingleValueSimulationData(value_name="balance")
        self.net_worth = SingleValueSimulationData(value_name="net_worth")
        self.stock_ownership = StockOwnershipData()
        self.data_collection.append(self.balance)
        self.data_collection.append(self.net_worth)
        self.data_collection.append(self.stock_ownership)

        # Adding buffer days.
        buffer = self.data_collection.get_buffer()
        from_date -= timedelta(days=buffer)

        # Setting date range for data collection.
        self.data_collection.set_date_range(from_date, to_date)
        self.data_collection.prepare_data()
        self.available_dates = self.data_collection.get_available_dates()

        # Setting duration range.
        max_duration = min(max_duration, len(self.available_dates))
        self.max_duration = max_duration if max_duration > 0 else len(self.available_dates)
        self.min_duration = min_duration if min_duration > 0 else self.max_duration
        self.min_duration = min(self.max_duration, self.min_duration)

        # Setting starting balance range.
        self.min_start_balance = min_start_balance
        self.max_start_balance = max_start_balance

        # Setting date tracking.
        self.curr_date_index = -1
        self.from_date_index = -1
        self.to_date_index = -1

        # Setting commission and max stock owned.
        self.commission = commission
        self.max_stock_owned = max_stock_owned

        # Setting up action space.
        self.action_space = gym.spaces.MultiBinary(len(self.data_collection.stock_names))

    @property
    def done(self):
        """Property, true if episode finished.
        """
        return self.curr_date_index >= self.to_date_index

    @property
    def observation(self):
        """Property for current observation.
        """
        return self.data_collection[self.available_dates[self.curr_date_index]]

    @property
    def reward(self):
        """Property for current reward.
        """
        return 0

    # pylint: disable=too-many-locals
    def step(self, action):
        """Simulate a single day of trading given the action.

        Args:
            action: a list of 1/0 (action/hold), where ith element shows what to do with ith stock.

        Returns:
            observation: a row of data source.
            reward: a number representing the reward associated with the action.
            done: True if the episode is finished
        """
        curr_date = self.available_dates[self.curr_date_index]
        next_date = self.available_dates[self.curr_date_index + 1]

        # Load state values
        balance = self.balance[curr_date].item()
        owned_stocks = self.stock_ownership[curr_date].copy().to_numpy()
        stock_prices = self.stock_data[curr_date].to_numpy()
        num_owned_stocks = np.count_nonzero(owned_stocks)
        if num_owned_stocks < self.max_stock_owned:
            max_purchase_price = balance / (self.max_stock_owned - num_owned_stocks)
            max_purchase_price /= 1 + self.commission
        else:
            max_purchase_price = 0

        # Simulate buy and sell actions
        sale_return = 0
        purchase_price = 0
        for index, sub_action in enumerate(action):
            if sub_action == 1:
                if owned_stocks[index] > 0:
                    sale_return += owned_stocks[index] * stock_prices[index]
                    owned_stocks[index] = 0
                elif num_owned_stocks < self.max_stock_owned:
                    num_stock_purchased = math.floor(max_purchase_price / stock_prices[index])
                    if num_stock_purchased > 0:
                        num_owned_stocks += 1
                    purchase_price += num_stock_purchased * stock_prices[index]
                    owned_stocks[index] = num_stock_purchased
        sale_return *= 1 - self.commission
        purchase_price *= 1 + self.commission
        balance = balance + sale_return - purchase_price

        # Update internal state vales.
        self.curr_date_index += 1
        self.balance[next_date] = balance
        self.net_worth[next_date] = balance + sum(owned_stocks * stock_prices)
        self.stock_ownership[next_date] = owned_stocks
        return self.observation, self.reward, self.done

    def reset(self):
        """Resets the simulation environment.
        """
        self.data_collection.reset()
        self.data_collection.prepare_data()

        # Setting from date, to date for the next episode.
        duration = random.randint(self.min_duration, self.max_duration)
        curr_date_index = random.randint(0, len(self.available_dates) - duration)
        self.from_date_index = curr_date_index
        self.curr_date_index = curr_date_index
        self.to_date_index = curr_date_index + duration - 1

        # Setting balance and net worth for the first day.
        curr_date = self.available_dates[curr_date_index]
        self.balance[curr_date] = random.randint(self.min_start_balance, self.max_start_balance)
        self.net_worth[curr_date] = self.balance[curr_date].item()
        return self.observation

    def render(self, mode="human"):
        """Renders current situation.

        Args:
            mode: something
        """
