"""Factory function for reward.
"""
from stock_trading_backend.simulation.constant_reward import ConstantReward


REWARD_CLASSES = [
    ConstantReward,
]
REWARD_NAME_MAPPING = {reward.name:reward for reward in REWARD_CLASSES}

def create_reward(reward_config, env):
    """Factory for reward objects.

    Args:
        reward_type: str with reward type.
        env: StockMarketSimulation for which the reward is created.
    """
    if reward_config["name"] not in REWARD_NAME_MAPPING:
        raise LookupError("Reward of type {} is not found.".format(reward_config["name"]))
    reward_name = reward_config["name"]
    del reward_config["name"]
    return REWARD_NAME_MAPPING[reward_name](env, **reward_config)
