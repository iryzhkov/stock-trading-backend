"""Class for storing stock ownership data from the simulation.
"""
import numpy as np
import pandas as pd

from stock_trading_backend.data.simulation_data import SimulationData


class StockOwnershipData(SimulationData):
    """Class for storing stock ownership data from the simulation.
    """
    name = "stock_ownership"

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
        self.data = pd.DataFrame(data=np.zeros((num_days, len(stock_names))),
                                 index=pd.date_range(from_date, to_date),
                                 columns=stock_names)
        # pylint: disable=unnecessary-lambda
        self.data.rename(lambda name: "owned_{}".format(name), axis=1, inplace=1)
        self.ready = True

    def reset(self, dependencies):
        """Reset for data object.

        Args:
            dependencies: The list of .ready values for the dependencies.

        Returns:
            The value of self.ready
        """
        self.ready = False
