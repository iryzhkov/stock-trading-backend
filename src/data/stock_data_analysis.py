"""Base class for storing stock data analysis.
"""
from src.data import Data, DataType


class StockDataAnalysis(Data):
    """Base class for storing stock data analysis.
    """
    data_type = DataType.STOCK_DATA_ANALYSIS
