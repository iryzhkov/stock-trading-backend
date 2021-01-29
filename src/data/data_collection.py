"""A class containing multiple Data classes.
"""
from src.data.data import DataType


# pylint: disable=too-few-public-methods
class DataCollection:
    """Class that contains multiple Data classes.
    """
    def __init__(self, data_objects, date_range, stock_names):
        """Initializer for DataCollection class.

        Args:
            data_objects: a list of Data objects. First object is used as main stock data provider.
            date_range: a tuple of dates that provides a range.
            stock_names: a list of stock names to prepare.
        """
        self.date_range = date_range
        self.stock_names = stock_names
        self.data_objects = data_objects
        if self.data_objects[0].data_type != DataType.STOCK_DATA:
            raise ValueError("Expected first data to be stock data.")

        self.id_to_data = {d.id_str:d for d in self.data_objects}
        if len(self.id_to_data) != len(self.data_objects):
            raise ValueError("Some data objects have conflicting ids.")

        self.stock_data_id = self.data_objects[0].id_str

        for data in self.data_objects:
            for dep in data.dependencies:
                if not dep in self.id_to_data:
                    raise LookupError("Couln't find {} (dependency of {})".format(dep, data.id_str))

    def _prepare_data(self, data_id):
        """Prepares a single data object.

        Args:
            data_id: the id of data to prepare.

        Returns:
            data object that was prepared.
        """
        data = self.id_to_data[data_id]
        if data.ready:
            return data

        stock_data = self.id_to_data[self.stock_data_id]
        dependencies = [self._prepare_data(dep_id) for dep_id in data.dependencies]
        data.prepare_data(self.date_range, self.stock_names, dependencies, stock_data)
        return data

    def prepare_data(self):
        """Prepares all the data in the collection.
        """
        self._prepare_data(self.stock_data_id)
        for id_str in self.id_to_data:
            self._prepare_data(id_str)
