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
    name = None
    data_type = DataType.NONE
    is_stock_specific = False
    expected_num_dependencies = 0

    def __init__(self, dependencies=None):
        """Initializer for Data class

        Args:
            dependencies: a list of dependency ids for the data.
        """
        self.id_str = self.name
        self.data = []
        self.ready = False
        if dependencies:
            self.dependencies = dependencies
        else:
            self.dependencies = []

        if len(self.dependencies) != self.expected_num_dependencies:
            raise ValueError("Expected {} dependencies, got {}".format(
                self.expected_num_dependencies, len(self.dependencies)))

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """

    def __getitem__(self, date):
        """Get the data for the date.

        Args:
            date: the specified lookup date.

        Returns:
            DataFrame row with the data.
        """
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
        return date in self.data

    def __iter__(self):
        """Iterator generator.

        Returns iterator object for the data.
        """
        return self.data.__iter__()
