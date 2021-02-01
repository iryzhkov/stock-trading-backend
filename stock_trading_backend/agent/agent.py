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

    # pylint: disable=no-self-use
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
        return balance, net_worth

    def make_decision(self, env):
        """Make decision based on the given data.
        """

    def apply_learning(self):
        """Applies learning if applicable for provided data.
        """

    def save_agent(self):
        """Saves the agent for future re-use.
        """

    def load_agent(self):
        """Loads the saved version of the agent.
        """
