"""Base class for stock market agent.
"""

class Agent():
    """Base class for stock market agent.
    """
    name = None
    requires_learning = False

    def __init__(self, data_collection_config):
        """Initializer for Agent.

        Args:
            data_collection_config: configuration for the data collection used by the agent.
        """
        self.data_collection_config = data_collection_config
        self.stock_names = data_collection_config["stock_names"]
        self.id_str = self.name

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
    def make_decision(self, observation, env):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
        """
        return env.action_space.sample()

    def apply_learning(self):
        """Applies learning if applicable for provided data.
        """

    def save_agent(self):
        """Saves the agent for future re-use.
        """

    def load_agent(self):
        """Loads the saved version of the agent.
        """
