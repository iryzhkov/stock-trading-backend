"""Base class for reward.
"""
class Reward():
    """Base class for reward.
    """
    name = "constant"

    # pylint: disable=unused-argument
    def __init__(self, env=None, default_value=0):
        """Initializer for reward class.

        Args:
            env: StockMarketSimulation enviroment for which the Reward is build.
            default_value: the default value to use for reward.
        """
        self.default_value = default_value
        self.reset()

    @property
    def value(self):
        """Property, returns current reward value.
        """
        return self.default_value

    def calculate_value(self, observation):
        """Calculates the value of the reward given the observation.

        Args:
            observation: observation from the environemnt.
        """

    def reset(self):
        """Resets the internal reward state.
        """
