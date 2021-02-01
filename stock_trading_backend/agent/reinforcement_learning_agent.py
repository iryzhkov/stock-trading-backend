"""Class for reinforcement learning based agent.
"""
from stock_trading_backend.agent import Agent

class ReinforcementLearningAgent(Agent):
    """Class for reinforcement learning based agent.
    """
    def __init__(self, agent_config, data_source_config):
        """Initializer for reinforcement learning based agent.

        Args:
            agent_config: configuration for an agent.
            data_source_config: configuration for a data source.
        """
        super(ReinforcementLearningAgent, self).__init__(data_source_config)
        self.agent_config = agent_config

    def make_decision(self):
        """Make decision based on the given data.
        """

    def load_model(self):
        """Loads model from storage.
        """

    def save_model(self):
        """Saves model to storage.
        """
