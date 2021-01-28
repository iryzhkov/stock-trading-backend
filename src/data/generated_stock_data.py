"""Class for storing generated stock data.
"""
from src.data.stock_data import StockData


class GeneratedStockData(StockData):
    """Class for storing generated stock data.
    """
    name = "generated_stock_data"

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
