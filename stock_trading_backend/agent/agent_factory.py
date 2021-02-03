"""Factory function for reward.
"""
from copy import deepcopy

from stock_trading_backend.agent.following_feature_agent import FollowingFeatureAgent

AGENT_CLASSES = [
    FollowingFeatureAgent,
]
AGENT_NAME_MAPPING = {agent.name:agent for agent in AGENT_CLASSES}

def create_agent(agent_config, data_collection_config, reward_config):
    """Factory for agent objects.

    Args:
        agnet_config: config for agent.
        data_collection_config: data collection config.
        reward_config: reward configuration for agent.
    """
    if agent_config["name"] not in AGENT_NAME_MAPPING:
        raise LookupError("Agent of type {} is not found.".format(agent_config["name"]))
    agent_config = deepcopy(agent_config)
    agent_name = agent_config["name"]
    del agent_config["name"]
    return AGENT_NAME_MAPPING[agent_name](data_collection_config=data_collection_config,
                                          reward_config=reward_config, **agent_config)
