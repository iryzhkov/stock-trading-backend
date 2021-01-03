"""Base class for storing data.
"""
from enum import Enum, auto

class DataType(Enum):
    """Enumerator class for types of data.
    """
    NONE = auto()
    STOCK_DATA = auto()
    STOCK_DATA_ANALYSIS = auto()
    SIMULATION_DATA = auto()


class Data:
    """Base class for storing data.
    """
    id = None
    data_type = DataType.NONE
    is_stock_specific = False

    def __init__(self):
        """Initializer for Data class
        """

    def get_data_for_date(self, date):
        """Get the data for the date.

        Args:
            date: the specified lookup date.

        Returns:
            DataFrame with the data.
        """

    def get_data_for_date_range(self, range_start, range_end):
        """Get the data for the date range.

        Args:
            range_start: the start of the range.
            range_end: the end of the range.

        Returns:
            DataFrame with the data.
        """
