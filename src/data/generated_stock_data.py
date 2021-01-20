"""Class for storing generated stock data.
"""
from src.data import StockData, DataType

class GeneratedStockData(StockData):
    """Class for storing generated stock data.
    """
    id = "generated_stock_data"
    data_type = DataType.STOCK_DATA
