"""Backtest.
"""
from datetime import datetime, timedelta

from stock_trading_backend.simulation import StockMarketSimulation

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
        overall reward for the backtest.
    """
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

    observation = simulation.reset()
    while not simulation.done:
        action = agent.make_decision(observation, simulation)
        observation, _, _ = simulation.step(action)
    return simulation.overall_reward
