"""Class for storing balance data from the simulation.
"""
from abc import ABCMeta

from src.data.simulation_data import SimulationData


# pylint: disable=too-few-public-methods
class SingleValueSimulationData(SimulationData, metaclass=ABCMeta):
    """Class for storing a single value from the simulation.
    """
    def __setitem__(self, date, value):
        """Setter for the value.

        Args:
            date: datetime date for which to set value
            value: new value.
        """
        self.data[date] = value
