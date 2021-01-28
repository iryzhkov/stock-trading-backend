"""Base class for storing stock data analysis.
"""
from src.data.data import Data, DataType


class StockDataAnalysis(Data):
    """Base class for storing stock data analysis.
    """
    data_type = DataType.STOCK_DATA_ANALYSIS

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
