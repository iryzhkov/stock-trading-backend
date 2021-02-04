"""Class for running a simulation.
"""
from datetime import datetime, timedelta

import random
import math
import itertools

import gym
import numpy as np
import pandas as pd

from stock_trading_backend.data import create_data_collection
from stock_trading_backend.simulation.reward_factory import create_reward
from stock_trading_backend.util import read_config_file

DEFAULT_DATA_COLLECTION_CONFIG_FILE = "data/default.yaml"

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

        Note: See data sub-package for more information.

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
        Reward can be set up with the reward_config parameter. Available rewards:

        Name                Description
        sharpe_ratio        Returns sharpe ratio for the agent. Only works with real stock data.
        net_worth_ratio     Returns net_worth growth ratio - 1. (default)
        constant            Returns the same value.

        Note: See reward classes for more information.

    Starting State:
        Agent starts with 0 stocks. The amount of money is selected uniformly in the given range.
        The date is selected uniformly in the date range. The length of the simulation is selected
        uniformly in the length range.

    Episode Termination:
        Episode length is greater than allowed.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, data_collection_config=None, from_date=None, to_date=None, min_duration=0,
                 max_duration=0, min_start_balance=1000, max_start_balance=1000, commission=0,
                 max_stock_owned=1, stock_data_randomization=False, reward_config=None):
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
            stock_data_randomization: whether to add stock data randomization.
            reward_config: the configuration for the reward.
        """
        if data_collection_config is None:
            data_collection_config = read_config_file(DEFAULT_DATA_COLLECTION_CONFIG_FILE)
        data_collection_config["stock_data_randomization"] = stock_data_randomization
        self.data_collection_config = data_collection_config

        if from_date is None and to_date is None:
            from_date = datetime(2014, 1, 1)
            to_date = datetime(2016, 1, 1)
        elif from_date is None or to_date is None:
            raise ValueError("Either both from and to dates are None or none of them.")

        self.data_collection = create_data_collection(data_collection_config)

        # Setup of simulation data.
        stock_data_id = self.data_collection.absolute_stock_data_id
        self.stock_data = self.data_collection.id_to_data[stock_data_id]
        self.stock_names = self.data_collection.stock_names
        self.balance = 0
        self.net_worth = 0
        self.owned_stocks = None

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

        # Setting up reward function.
        if reward_config is None:
            reward_config = {"name": "net_worth_ratio_reward"}
        self.reward_function = create_reward(reward_config, from_date, to_date)

        # Setting up observation cache.
        self.saved_date_index = -1
        self.saved_observation = None

    def action_space_generator(self):
        """Generator for action space.

        Takes into account max stocks owned.

        If you want to iterate over all legitimate actions use this.

        Returns:
            Generator obejct with all possible actions.
        """
        num_owned_stocks = np.count_nonzero(self.owned_stocks)
        num_not_owned_stocks = len(self.owned_stocks) - num_owned_stocks
        num_possible_to_purchase = self.max_stock_owned - num_owned_stocks

        for num_purchases in range(num_possible_to_purchase + 1):
            indexes_iter = itertools.combinations(range(num_not_owned_stocks), num_purchases)
            for indexes in indexes_iter:
                sell_actions = itertools.product([0, 1], repeat=num_owned_stocks)
                purchase_action = [0] * num_not_owned_stocks
                for i in indexes:
                    purchase_action[i] = 1
                for sell_action in sell_actions:
                    action = [0] * len(self.owned_stocks)
                    sell_index, purchase_index = 0, 0
                    for i, owned_num in enumerate(self.owned_stocks):
                        if owned_num > 0:
                            action[i] = sell_action[sell_index]
                            sell_index += 1
                        else:
                            action[i] = purchase_action[purchase_index]
                            purchase_index += 1
                    yield action

    @property
    def overall_reward(self):
        """Property, returns overall reward for the current episode.
        """
        return self.reward_function.calculate_overall_reward()

    @property
    def done(self):
        """Property, true if episode finished.
        """
        return self.curr_date_index >= self.to_date_index

    @property
    def observation(self):
        """Property for current observation.
        """
        if self.saved_date_index == self.curr_date_index:
            return self.saved_observation

        self.saved_date_index = self.curr_date_index
        owned_stocks = pd.Series(self.owned_stocks,
                                 ["owned_{}".format(name) for name in self.stock_names])
        balance_and_net_worth = pd.Series([self.balance, self.net_worth], ["balance", "net_worth"])
        data = self.data_collection[self.available_dates[self.curr_date_index]]
        self.saved_observation = pd.concat([owned_stocks, balance_and_net_worth, data])
        return self.saved_observation

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
        stock_prices = self.stock_data[curr_date].to_numpy()
        num_owned_stocks = np.count_nonzero(self.owned_stocks)
        if num_owned_stocks < self.max_stock_owned:
            max_purchase_price = self.balance / (self.max_stock_owned - num_owned_stocks)
            max_purchase_price /= 1 + self.commission
        else:
            max_purchase_price = 0

        # Simulate buy and sell actions
        sale_return = 0
        purchase_price = 0
        for index, sub_action in enumerate(action):
            if sub_action == 1:
                if self.owned_stocks[index] > 0:
                    sale_return += self.owned_stocks[index] * stock_prices[index]
                    self.owned_stocks[index] = 0
                elif num_owned_stocks < self.max_stock_owned:
                    num_stock_purchased = math.floor(max_purchase_price / stock_prices[index])
                    if num_stock_purchased > 0:
                        num_owned_stocks += 1
                    purchase_price += num_stock_purchased * stock_prices[index]
                    self.owned_stocks[index] = num_stock_purchased
        sale_return *= 1 - self.commission
        purchase_price *= 1 + self.commission
        self.balance += sale_return - purchase_price

        # Update internal state vales.
        self.curr_date_index += 1
        self.net_worth = self.balance + sum(self.owned_stocks * stock_prices)
        reward = self.reward_function.calculate_value(self.observation, next_date)
        return self.observation, reward, self.done

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
        self.balance = random.randint(self.min_start_balance, self.max_start_balance)
        self.net_worth = self.balance
        self.owned_stocks = np.zeros(len(self.stock_names))

        # Reset observation cache.
        self.saved_date_index = -1
        self.saved_observation = None

        # Reset the reward function.
        self.reward_function.reset(self.observation, curr_date)
        return self.observation

    def render(self, mode="human"):
        """Renders current situation.

        Args:
            mode: something
        """
