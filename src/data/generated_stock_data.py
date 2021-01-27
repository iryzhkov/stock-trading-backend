"""Class for storing generated stock data.
"""
from src.data import StockData, DataType


class GeneratedStockData(StockData):
    """Class for storing generated stock data.
    """
    id = "generated_stock_data"
    data_type = DataType.STOCK_DATA

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
