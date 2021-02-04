"""APIs for the package.
"""
import os

from stock_trading_backend.agent import create_agent
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

def get_agent_config(agent_name):
    """Get agent config.

    Args:
        agent_name: string, name of the agent (returned from get_available_agents).

    Returns:
        A config to use for agent factory.
    """
    return read_config_file(os.path.join("agent", agent_name + ".yaml"))

def get_available_data_collections():
    """Gets a list of data collection set ups.

    Returns:
        List of strings with data collection set up names.
    """
    return _get_list_of_config_names("data")

def get_data_collection_config(data_collection_name):
    """Get data collection config.

    Args:
        agent_name: string, name of the agent (returned from get_available_agents).
        data_collection_name: string, name of the data collection set up.
        reward_name: string, name of the reward (returned from get_available_rewards).
        model_name: string, name of the model to use (returned from get_available_models).

    Returns:
        A config to use for data collection factory.
    """
    return read_config_file(os.path.join("data", data_collection_name + ".yaml"))

def get_available_rewards():
    """Gets a list of available reward set ups.

    Returns:
        List of string with reward names.
    """
    return _get_list_of_config_names("reward")

def get_reward_config(reward_name):
    """Get reward config.

    Args:
        reward_name: string, name of the reward (returned from get_available_rewards).

    Returns:
        A config to use for reward factory.
    """
    return read_config_file(os.path.join("reward", reward_name + ".yaml"))

def get_available_models():
    """Gets a list of available models.

    Returns:
        List of string with model names.
    """
    return _get_list_of_config_names("model")

def get_model_config(model_name):
    """Get model config.

    Args:
        model_name: string, name of the model to use (returned from get_available_models).

    Returns:
        A config to use for model factory.
    """
    if model_name is None:
        return None
    return read_config_file(os.path.join("model", model_name + ".yaml"))

def get_agent_object(agent_name="following_feature_agent_1", data_collection_name="default",
                     reward_name="net_worth_ratio", model_name=None):
    """Creates an agent with provided agent name and data collection name.

    Args:
        agent_name: string, name of the agent (returned from get_available_agents).
        data_collection_name: string, name of the data collection set up.
        reward_name: string, name of the reward (returned from get_available_rewards).
        model_name: string, name of the model to use (returned from get_available_models).

    Returns:
        Agent object.
    """
    data_collection_config = get_data_collection_config(data_collection_name)
    agent_config = get_agent_config(agent_name)
    reward_config = get_reward_config(reward_name)
    model_config = get_model_config(model_name)
    agent = create_agent(agent_config, data_collection_config, reward_config, model_config)
    return agent
