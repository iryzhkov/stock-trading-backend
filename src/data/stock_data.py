"""Base class for storing stock data.
"""
from src.data import Data, DataType

class StockData(Data):
    """Base class for storing stock data.
    """
    id = None
    data_type = DataType.STOCK_DATA
    is_stock_specific = True
