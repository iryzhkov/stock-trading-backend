"""Class for storing randomized stock data.
"""
import numpy as np

from src.data.stock_data import StockData


class RandomizedStockData(StockData):
    """Class for storing randomized stock data.
    """
    name = "randomized_stock_data"
    expected_num_dependencies = 1

    def __init__(self, dependencies=None, mean=0, stdev=0.025):
        """Initializer for Randomized Stock Data class

        Args:
            dependencies: a list of dependency ids for the data.
            mean: the mean relative difference for the randomized data.
            stdev: the standart deviation for the relative difference.
        """
        super(RandomizedStockData, self).__init__(dependencies)
        self.id_str = "randomized_{}".format(self.dependencies[0])
        self.mean = mean
        self.stdev = stdev

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """
        self.ready = True
        other_data = dependencies[0].data
        noise = 1 + np.random.normal(self.mean, self.stdev, [len(other_data), len(stock_names)])
        self.data = other_data.copy() * noise

    def reset(self, dependencies):
        """Reset for randomized stock data.

        Args:
            dependencies: The list of .ready values for the dependencies.

        Returns:
            The value of self.ready
        """
        self.ready = False
        return self.ready
