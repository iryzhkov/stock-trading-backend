"""Class for storing real stock data.
"""
from src.data.stock_data import StockData


class RealStockData(StockData):
    """Class for storing real stock data.
    """
    name = "real_stock_data"

    def prepare_data(self, date_range, stock_names, dependencies):
        """Data preparation for real stock data.

        Gets the data prepared.

        Args:
            date_range: a tuple of dates that provides a range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared dependencies.
        """
        self.ready = True

    def reset(self):
        """Stuff to run
        """
