"""Class for storing balance data from the simulation.
"""
from src.data.single_value_simulation_data import SingleValueSimulationData


# pylint: disable=too-few-public-methods
class BalanceData(SingleValueSimulationData):
    """Class for storing balance data from the simulation.
    """
    name = "balance"

    def __setitem__(self, date, value):
        """Setter for BalanceData.

        Args:
            date: datetime date for which to set value
            value: new value.
        """
        self.data[date] = value
