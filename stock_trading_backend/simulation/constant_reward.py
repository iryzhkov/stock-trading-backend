"""Class for constant reward.
"""
from stock_trading_backend.simulation.reward import Reward


class ConstantReward(Reward):
    """Constant reward class.
    """
    name = "constant"

    # pylint: disable=unused-argument
    def __init__(self, env=None, value=0):
        """Initializer for reward class.

        Args:
            env: StockMarketSimulation enviroment for which the Reward is build.
            default_value: the default value to use for reward.
        """
        self.value = value

    def calculate_value(self, observation, date):
        """Returns the value set in the initialization.

        Args:
            observation: the state of the environment.
            date: datetime current date in the environment
        """
        return self.value
