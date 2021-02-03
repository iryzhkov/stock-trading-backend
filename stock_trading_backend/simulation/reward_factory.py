"""Factory function for reward.
"""
from copy import deepcopy

from stock_trading_backend.simulation.constant_reward import ConstantReward
from stock_trading_backend.simulation.net_worth_ratio_reward import NetWorthRatioReward
from stock_trading_backend.simulation.sharpe_ratio_reward import SharpeRatioReward


REWARD_CLASSES = [
    ConstantReward,
    NetWorthRatioReward,
    SharpeRatioReward,
]
REWARD_NAME_MAPPING = {reward.name:reward for reward in REWARD_CLASSES}

def create_reward(reward_config, from_date, to_date):
    """Factory for reward objects.

    Args:
        reward_type: str with reward type.
        from_date: datetime start of the date range.
        to_date: datetime end of the date range.
    """
    if reward_config["name"] not in REWARD_NAME_MAPPING:
        raise LookupError("Reward of type {} is not found.".format(reward_config["name"]))
    reward_config = deepcopy(reward_config)
    reward_name = reward_config["name"]
    del reward_config["name"]
    return REWARD_NAME_MAPPING[reward_name](from_date=from_date, to_date=to_date, **reward_config)
