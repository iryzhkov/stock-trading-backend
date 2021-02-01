"""Base class for storing data from the simulation.
"""
from abc import ABCMeta
from stock_trading_backend.data.data import Data, DataType


# pylint: disable=too-few-public-methods
class SimulationData(Data, metaclass=ABCMeta):
    """Base class for storing data from the simulation.
    """
    data_type = DataType.SIMULATION_DATA

    def __init__(self, dependencies=None, visible=True):
        """Initializer for Generated Stock Data class

        Args:
            dependencies: a list of dependency ids for the data.
            visible: whether the data is visible in data_collection[date].
        """
        super(SimulationData, self).__init__(dependencies, visible)
