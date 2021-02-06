"""Backtest.
"""
from datetime import datetime, timedelta

import numpy as np

from stock_trading_backend.simulation import StockMarketSimulation

# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
def backtest_agent(agent, from_date=None, to_date=None, start_balance=1000, commission=0,
                   max_stock_owned=1):
    """Backtests an agent with provided params.

    Args:
        from_date: datetime date for the start of the range.
        to_date: datetime date for the end of the range.
        start_balance: the starting balance.
        commission: relative commission for each transcation.
        max_stock_owned: a maximum number of different stocks that can be owned.

    Returns:
        reward: overall reward for the backtest.
        net_worth_history: a list of net worth values.
        balance_history: a list of balance values.
        owned_stocks_history: a list of lists of owned stocks.
        action_history: a list of lists of actions (1 for buy, 0 for hold, -1 for sell).
        price_history: a list of stock prices.
    """
    if not agent.usable:
        raise ValueError("Agent is not ready for back-testing.")

    if from_date is None or to_date is None:
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        from_date = today - timedelta(days=60)
        to_date = today - timedelta(days=1)

    simulation = StockMarketSimulation(agent.data_collection_config, from_date=from_date,
                                       to_date=to_date, min_start_balance=start_balance,
                                       max_start_balance=start_balance, commission=commission,
                                       max_stock_owned=max_stock_owned,
                                       reward_config=agent.reward_config)

    net_worth_history = []
    balance_history = []
    owned_stocks_history = []
    stock_price_history = []

    def record_history():
        balance, net_worth, owned_stocks, _ = agent.unpack_observation(observation)
        curr_date = simulation.available_dates[simulation.curr_date_index]
        stock_prices = simulation.stock_data[curr_date].to_numpy()

        # pylint: disable=no-member
        net_worth_history.append(net_worth)
        # pylint: disable=no-member
        balance_history.append(balance)
        # pylint: disable=no-member
        owned_stocks_history.append(owned_stocks)
        # pylint: disable=no-member
        stock_price_history.append(stock_prices)

    observation = simulation.reset()
    while not simulation.done:
        record_history()
        action, _ = agent.make_decision(observation, simulation)
        observation, _, _ = simulation.step(action)

    record_history()
    net_worth_history = np.array(net_worth_history)
    balance_history = np.array(balance_history)
    owned_stocks_history = np.array(owned_stocks_history)
    stock_price_history = np.array(stock_price_history)
    action_history = owned_stocks_history[1:] - owned_stocks_history[:-1]

    output = {
        "reward": simulation.overall_reward,
        "stock_names": simulation.stock_names,
        "net_worth_history": net_worth_history,
        "balance_history": balance_history,
        "owned_stocks_history": owned_stocks_history,
        "action_history": action_history,
        "stocks_price_history": stock_price_history,
    }
    return output
