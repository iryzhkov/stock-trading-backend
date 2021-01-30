"""Class for storing net worth data from the simulation.
"""
from src.data.single_value_simulation_data import SingleValueSimulationData


# pylint: disable=too-few-public-methods
class NetWorthData(SingleValueSimulationData):
    """Class for storing net worth data from the simulation.
    """
    name = "net_worth"
