"""A class containing multiple Data classes.
"""
from src.data.data import DataType


# pylint: disable=too-few-public-methods
class DataCollection:
    """Class that contains multiple Data classes.
    """
    def __init__(self, data_objects, stock_names):
        """Initializer for DataCollection class.

        Args:
            data_objects: a list of Data objects. First object is used as main stock data provider.
            stock_names: a list of stock names to prepare.
        """
        self.stock_names = stock_names
        self.data_objects = data_objects
        if self.data_objects[0].data_type != DataType.STOCK_DATA:
            raise ValueError("Expected first data to be stock data.")

        self.id_to_data = {d.id_str:d for d in self.data_objects}
        self.busy = {d.id_str:False for d in self.data_objects}
        if len(self.id_to_data) != len(self.data_objects):
            raise ValueError("Some data objects have conflicting ids.")

        self.stock_data_id = self.data_objects[0].id_str

        for data in self.data_objects:
            for i, dep in enumerate(data.dependencies):
                if dep == "stock_data":
                    data.dependencies[i] = self.stock_data_id
                elif not dep in self.id_to_data:
                    raise LookupError("Couln't find {} (dependency of {})".format(dep, data.id_str))

    def _prepare_data(self, data_id, from_date, to_date):
        """Prepares a single data object.

        Args:
            data_id: the id of data to prepare.
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.

        Returns:
            data object that was prepared.
        """
        if self.busy[data_id]:
            raise ValueError("Circular dependency detected.")

        data = self.id_to_data[data_id]
        if data.ready:
            return data

        self.busy[data_id] = True
        dependencies = [self._prepare_data(dep_id, from_date, to_date)
                        for dep_id in data.dependencies]
        data.prepare_data(from_date, to_date, self.stock_names, dependencies)
        self.busy[data_id] = False
        return data

    def prepare_data(self, from_date, to_date):
        """Prepares all the data in the collection.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
        """
        for id_str in self.id_to_data:
            self._prepare_data(id_str, from_date, to_date)
