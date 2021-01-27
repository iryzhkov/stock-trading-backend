"""Base class for storing data.
"""
from abc import ABCMeta
from enum import Enum, auto

class DataType(Enum):
    """Enumerator class for types of data.
    """
    NONE = auto()
    STOCK_DATA = auto()
    STOCK_DATA_ANALYSIS = auto()
    SIMULATION_DATA = auto()


class Data(metaclass=ABCMeta):
    """Base class for storing data.
    """
    id = None
    data_type = DataType.NONE
    is_stock_specific = False

    def __init__(self):
        """Initializer for Data class
        """
        self.data = []

    def __getitem__(self, date):
        """Get the data for the date.

        Args:
            date: the specified lookup date.

        Returns:
            DataFrame row with the data.
        """
        if self.data is None:
            raise Exception("data is not defined.")

        if date not in self.data:
            raise LookupError("{} is not in the data".format(date))

        return self.data[date]

    def __len__(self):
        """Get the size of the data.

        Returns:
            A number of rows in the self.data
        """
        return len(self.data)

    def __contains__(self, date):
        """Checks if date is in self.data.

        Args:
            date: the specified lookup date.

        Returns:
            Whether the date is in self.data
        """
        if self.data is None:
            raise Exception("data is not defined.")

        return date in self.data

    def __iter__(self):
        """Iterator.

        Args:
            date: the specified lookup date.

        Returns:
            Whether the date is in self.data
        """
        if self.data is None:
            raise Exception("data is not defined.")

        return self.data.__iter__()
