"""Class for storing randomized stock data.
"""
from src.data.stock_data import StockData


# pylint: disable=too-few-public-methods
class RandomizedStockData(StockData):
    """Class for storing randomized stock data.
    """
    name = "randomized_stock_data"
    expected_num_dependencies = 1

    def __init__(self, dependencies=None):
        """Initializer for Randomized Stock Data class

        Args:
            dependencies: a list of dependency ids for the data.
        """
        super(RandomizedStockData, self).__init__(dependencies)
        self.id_str = "randomized_{}".format(self.dependencies[0])

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
