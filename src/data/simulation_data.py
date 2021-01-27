"""Base class for storing simulation data.
"""
from src.data import Data, DataType


class SimulationData(Data):
    """Base class for storing simulation data.
    """
    data_type = DataType.SIMULATION_DATA

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
