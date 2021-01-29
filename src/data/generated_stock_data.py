"""Class for storing generated stock data.
"""
from src.data.stock_data import StockData


# pylint: disable=too-few-public-methods
class GeneratedStockData(StockData):
    """Class for storing generated stock data.
    """
    name = "generated_stock_data"

    def prepare_data(self, date_range, stock_names, dependencies, stock_data):
        """Data preparation.

        Gets the data prepared.

        Args:
            date_range: a tuple of dates that provides a range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
            stock_data: a Data object with stock data.
        """
        self.ready = True
