"""Factory function for agents.
"""
from copy import deepcopy

from stock_trading_backend.agent.following_feature_agent import FollowingFeatureAgent
from stock_trading_backend.agent.sarsa_learning_agent import SARSALearningAgent
from stock_trading_backend.agent.q_learning_agent import QLearningAgent

AGENT_CLASSES = [
    FollowingFeatureAgent,
    SARSALearningAgent,
    QLearningAgent,
]
AGENT_NAME_MAPPING = {agent.name:agent for agent in AGENT_CLASSES}

def create_agent(agent_config, data_collection_config, reward_config, model_config=None):
    """Factory for agent objects.

    Args:
        agnet_config: config for agent.
        data_collection_config: data collection config.
        reward_config: reward configuration for agent.
        model_config: model configuration for agent
    """
    if agent_config["name"] not in AGENT_NAME_MAPPING:
        raise LookupError("Agent of type {} is not found.".format(agent_config["name"]))
    agent_config = deepcopy(agent_config)
    agent_name = agent_config["name"]
    del agent_config["name"]
    return AGENT_NAME_MAPPING[agent_name](data_collection_config=data_collection_config,
                                          reward_config=reward_config, model_config=model_config,
                                          **agent_config)
