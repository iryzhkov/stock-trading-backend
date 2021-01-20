"""Class for storing randomized stock data.
"""
from src.data import StockData, DataType

class RandomizedStockData(StockData):
    """Class for storing randomized stock data.
    """
    id = "randomized_stock_data"
    data_type = DataType.STOCK_DATA
