"""APIs for the package.
"""
from datetime import datetime, timedelta
import os

from stock_trading_backend.agent import create_agent
from stock_trading_backend.util import read_config_file
from stock_trading_backend.simulation import StockMarketSimulation

ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT, "config")

def _get_list_of_config_names(path):
    """Gets a list of configuration files in a path.

    Args:
        path: a path where to look.

    Returns:
        List of strings wi
    """
    path = os.path.join(CONFIG_PATH, path)
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    names = [file[:-5] for file in files if file.endswith("yaml")]
    return names

def get_available_agents():
    """Gets a list of available agents.

    Returns:
        List of strings with agent names.
    """
    return _get_list_of_config_names("agent")

def get_available_data_collections():
    """Gets a list of data collection set ups.

    Returns:
        List of strings with data collection set up names.
    """
    return _get_list_of_config_names("data")

def get_agent_object(agent_name, data_collection_name="default"):
    """Creates an agent with provided agent name and data collection name.

    Args:
        agent_name: string, name of the agent (returned from get_available_agents).
        data_collection_name: string, name of the data collection set up.

    Returns:
        Agent object.
    """
    data_collection_config = read_config_file(os.path.join("data", data_collection_name + ".yaml"))
    agent_config = read_config_file(os.path.join("agent", agent_name + ".yaml"))
    agent = create_agent(agent_config, data_collection_config)
    return agent

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
    """
    if from_date is None or to_date is None:
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        from_date = today - timedelta(days=60)
        to_date = today - timedelta(days=1)

    simulation = StockMarketSimulation(agent.data_collection_config, from_date=from_date,
                                       to_date=to_date, min_start_balance=start_balance,
                                       max_start_balance=start_balance, commission=commission,
                                       max_stock_owned=max_stock_owned)

    observation = simulation.reset()
    while not simulation.done:
        action = agent.make_decision(observation, simulation)
        observation, _, _ = simulation.step(action)
    return observation
