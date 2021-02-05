"""An agent that tries to follow a feature as its policy.
"""
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

    def __init__(self, data_collection_config, reward_config, model_config=None, features=None):
        """Initializer for FollowingFeatureAgent class.

        Args:
            data_collection_config: configuration for the data collection used by the agent.
            reward_config: configuration for reward used by the agent.
            model_config: configuration for model used by the agent.
            features: list of data configs, the first one is used for following.
        """
        super(FollowingFeatureAgent, self).__init__(data_collection_config, reward_config=None,
                                                    model_config=None)
        features[0]["visible"] = True
        data_collection_config["data"] += features
        followed_data = create_data(features[0])
        self.feature_template = followed_data.feature_template

    # pylint: disable=unused-argument
    def make_decision(self, observation, env, training=False):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
            training: boolean flag for specifying if this is training or testing.
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
