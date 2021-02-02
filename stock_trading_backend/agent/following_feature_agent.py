"""An agent that tries to follow a feature as its policy.
"""
import copy

from stock_trading_backend.agent.agent import Agent
from stock_trading_backend.data import create_data

class FollowingFeatureAgent(Agent):
    """An agent that tries to follow a feature as its poicy.

    e.g. if feature for STOCK_1 is > 0, than it will buy/hold STOCK_1. Otherwise it will sell
    STOCK_1.

    Note:
        This is example of non-reinforcement learning agent.
    """
    name = "following_feature_agent"

    def __init__(self, data_collection_config, features=None):
        """Initializer for FollowingFeatureAgent class.

        Args:
            env: StockTradingSimulation environment.
            features: a list of data configs. The first one is going to be followed.
        """
        super(FollowingFeatureAgent, self).__init__(data_collection_config)
        features[0]["visible"] = True
        data_collection_config["data"] += features
        followed_data = create_data(copy.copy(features[0]))
        self.feature_template = followed_data.feature_template

    def make_decision(self, observation, env):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
        """
        # Prepare information for decision making.
        _, _, owned_stocks, _ = self.unpack_observation(observation)
        feature = self.extract_stock_feature(observation, self.feature_template)

        action = [0] * len(owned_stocks)
        for stock_index, num_owned in enumerate(owned_stocks):
            if feature[stock_index] > 0 == num_owned:
                action[stock_index] = 1
            elif feature[stock_index] <= 0 < num_owned:
                action[stock_index] = 1

        return action
