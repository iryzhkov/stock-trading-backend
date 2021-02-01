"""Base class for storing stock data analysis.
"""
from abc import ABCMeta
from stock_trading_backend.data.data import Data, DataType


# pylint: disable=too-few-public-methods
class StockDataAnalysis(Data, metaclass=ABCMeta):
    """Base class for storing stock data analysis.
    """
    data_type = DataType.STOCK_DATA_ANALYSIS

    # pylint: disable=useless-super-delegation
    def __init__(self, dependencies=None, visible=True):
        """Initializer for Generated Stock Data class

        Args:
            dependencies: a list of dependency ids for the data.
            visible: whether the data is visible in data_collection[date].
        """
        super(StockDataAnalysis, self).__init__(dependencies, visible)
