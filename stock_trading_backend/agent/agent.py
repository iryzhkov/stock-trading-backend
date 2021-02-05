"""Base class for stock market agent.
"""
from abc import ABCMeta


class Agent(metaclass=ABCMeta):
    """Base class for stock market agent.
    """
    name = None
    requires_learning = False

    def __init__(self, data_collection_config, reward_config=None, model_config=None):
        """Initializer for Agent.

        Args:
            data_collection_config: configuration for the data collection used by the agent.
            reward_config: configuration for reward used by the agent.
            model_config: configuration for model used by the agent.
        """
        self.data_collection_config = data_collection_config
        self.reward_config = reward_config
        self.model_config = model_config
        self.stock_names = data_collection_config["stock_names"]
        self.id_str = self.name
        self.trained = False

    @property
    def usable(self):
        """Returns true if the agent can be used for backtesting.
        """
        return not self.requires_learning or self.trained

    def extract_stock_feature(self, observation, feature_template=""):
        """Extracts stock feature from observation.

        Feature is expected to be: feature_template.format(stock_name)

        Args:
            observation: observation to extract feature from.
            feature_template: what the feature key looks like.
        """
        return [observation[feature_template.format(stock_name)] for stock_name in self.stock_names]

    def unpack_observation(self, observation):
        """Unpacks observation into: balance, net_worth, owned_stocks, stock_prices.

        Note:
            This is mostly usefull for non-reinforcement learning agents.

        Args:
            observation: pandas Series with observation data.

        Returns:
            balance, net worth, owned_stocks, stock_prices
        """
        balance = observation["balance"]
        net_worth = observation["net_worth"]
        stock_prices = self.extract_stock_feature(observation, "{}")
        owned_stocks = self.extract_stock_feature(observation, "owned_{}")
        return balance, net_worth, owned_stocks, stock_prices

    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def make_decision(self, observation, env, training=False):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
            training: boolean flag for specifying if this is training or testing.
        """
        return env.action_space.sample()

    def apply_learning(self, observations, actions, rewards):
        """Applies learning for provided data.

        Args:
            observations: DataFrame with observations.
            actions: a list of actions.
            rewards: a list of rewards.

        Returns:
            Loss after training.
        """

    def save_agent(self):
        """Saves the agent for future re-use.
        """

    def load_agent(self):
        """Loads the saved version of the agent.
        """
