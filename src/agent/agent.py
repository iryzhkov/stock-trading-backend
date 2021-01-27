"""Base class for stock market agent.
"""

class Agent():
    """Base class for stock market agent.
    """
    def __init__(self, data_source_config):
        """Initializer for Agent.

        Args:
            data_source_config: configuration for the data source used by the agent.
        """
        self.data_source_config = data_source_config

    def make_decision(self):
        """Make decision based on the given data.
        """

    def apply_learning(self):
        """Applies learning if applicable for provided data.
        """
