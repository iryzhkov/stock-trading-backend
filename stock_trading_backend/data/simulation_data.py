"""Base class for storing data from the simulation.
"""
from abc import ABCMeta
from stock_trading_backend.data.data import Data, DataType


# pylint: disable=too-few-public-methods
class SimulationData(Data, metaclass=ABCMeta):
    """Base class for storing data from the simulation.
    """
    data_type = DataType.SIMULATION_DATA
