"""Base class for storing stock data.
"""
from abc import ABCMeta
from src.data.data import Data, DataType


class StockData(Data, metaclass=ABCMeta):
    """Base class for storing stock data.
    """
    data_type = DataType.STOCK_DATA
    is_stock_specific = True
