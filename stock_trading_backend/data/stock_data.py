"""Base class for storing stock data.
"""
from abc import ABCMeta
from stock_trading_backend.data.data import Data, DataType


# pylint: disable=too-few-public-methods
class StockData(Data, metaclass=ABCMeta):
    """Base class for storing stock data.
    """
    data_type = DataType.STOCK_DATA
    is_stock_specific = True
