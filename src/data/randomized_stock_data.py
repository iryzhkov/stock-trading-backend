"""Class for storing randomized stock data.
"""
from src.data import StockData, DataType


class RandomizedStockData(StockData):
    """Class for storing randomized stock data.
    """
    id = "randomized_stock_data"
    data_type = DataType.STOCK_DATA

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
