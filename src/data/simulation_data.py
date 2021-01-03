"""Base class for storing simulation data.
"""
from src.data import Data, DataType

class SimulationData(Data):
    """Base class for storing simulation data.
    """
    data_type = DataType.SIMULATION_DATA
