"""Base class for storing stock data analysis.
"""
from abc import ABCMeta
from src.data.data import Data, DataType


class StockDataAnalysis(Data, metaclass=ABCMeta):
    """Base class for storing stock data analysis.
    """
    data_type = DataType.STOCK_DATA_ANALYSIS
