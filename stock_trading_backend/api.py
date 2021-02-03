"""APIs for the package.
"""
from datetime import datetime, timedelta
import os

from stock_trading_backend.agent import create_agent
from stock_trading_backend.backtest import backtest_agent
from stock_trading_backend.simulation import StockMarketSimulation
from stock_trading_backend.util import read_config_file

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

def get_available_rewards():
    """Gets a list of available reward set ups.

    Returns:
        List of string with reard names.
    """
    return _get_list_of_config_names("reward")

def get_agent_object(agent_name="following_feature_agent_1", data_collection_name="default",
                     reward_name="net_worth_ratio"):
    """Creates an agent with provided agent name and data collection name.

    Args:
        agent_name: string, name of the agent (returned from get_available_agents).
        data_collection_name: string, name of the data collection set up.
        reward_name: string, name of the reward (returned from get_available_rewards).

    Returns:
        Agent object.
    """
    data_collection_config = read_config_file(os.path.join("data", data_collection_name + ".yaml"))
    agent_config = read_config_file(os.path.join("agent", agent_name + ".yaml"))
    reward_config = read_config_file(os.path.join("reward", reward_name + ".yaml"))
    agent = create_agent(agent_config, data_collection_config, reward_config)
    return agent
