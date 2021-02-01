"""Class for storing balance data from the simulation.
"""
import numpy as np
import pandas as pd

from stock_trading_backend.data.simulation_data import SimulationData


# pylint: disable=too-few-public-methods
class SingleValueSimulationData(SimulationData):
    """Class for storing a single value from the simulation.
    """
    def __init__(self, dependencies=None, value_name=""):
        """Initializer for Single Value Simulation Data class

        Args:
            dependencies: a list of dependency ids for the data.
            num_days: number of days to take the average of.
        """
        super(SingleValueSimulationData, self).__init__(dependencies)
        self.name = value_name
        self.id_str = self.name

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """
        num_days = (to_date - from_date).days + 1
        self.data = pd.DataFrame(data=np.zeros(num_days),
                                 index=pd.date_range(from_date, to_date),
                                 columns=[self.name])
        self.ready = True

    def reset(self, dependencies):
        """Reset for data object.

        Args:
            dependencies: The list of .ready values for the dependencies.

        Returns:
            The value of self.ready
        """
        self.ready = False
