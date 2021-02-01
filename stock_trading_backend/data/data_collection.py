"""A class containing multiple Data classes.
"""
import pandas as pd
from stock_trading_backend.data.data import DataType
from stock_trading_backend.data.randomized_stock_data import RandomizedStockData


# pylint: disable=too-many-instance-attributes
class DataCollection:
    """Class that contains multiple Data classes.
    """
    def __init__(self, data_objects, stock_names, stock_data_randomization=False):
        """Initializer for DataCollection class.

        Args:
            data_objects: a list of Data objects. First object is used as main stock data provider.
            stock_names: a list of stock names to prepare.
            stock_data_randomization: whether to add stock data randomization.
        """
        self.stock_names = stock_names
        self.data_objects = []
        self.visible_data_objects = []
        self.id_to_data = {}

        if data_objects[0].data_type != DataType.STOCK_DATA:
            raise ValueError("Expected first data to be stock data.")
        self.stock_data_id = data_objects[0].id_str

        if stock_data_randomization and not isinstance(data_objects[0], RandomizedStockData):
            randomization_layer = RandomizedStockData(dependencies=[self.stock_data_id])
            self.stock_data_id = randomization_layer.id_str
            data_objects.insert(0, randomization_layer)

        self.visible_data_objects.append(data_objects[0])

        # Helper attributes for recursive apply.
        self.busy = {}
        self.done = {}
        self.recursive_counter = 0

        for data in data_objects:
            self.append(data)

        self.from_date = None
        self.to_date = None

        for data in self.data_objects:
            for i, dep in enumerate(data.dependencies):
                if not dep in self.id_to_data:
                    raise LookupError("Couln't find {} (dependency of {})".format(dep, data.id_str))

    def append(self, data_object):
        """Helper function to add a new data object to the collection.

        Args:
            data_object: A Data object to add.
            index: A position where to insert.

        Returns:
            data_object that is used by data collection.
        """
        if data_object.id_str not in self.id_to_data:
            self.data_objects.append(data_object)
            for i, dep in enumerate(data_object.dependencies):
                if dep == "stock_data":
                    data_object.dependencies[i] = self.stock_data_id

            self.id_to_data[data_object.id_str] = data_object
            self.busy[data_object.id_str] = False
            self.done[data_object.id_str] = False

            if data_object.visible and data_object not in self.visible_data_objects:
                self.visible_data_objects.append(data_object)
        return self.id_to_data[data_object.id_str]

    def set_date_range(self, from_date, to_date):
        """Setter for date range.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
        """
        self.from_date = from_date
        self.to_date = to_date

    def get_available_dates(self):
        """Returns a list of available dates for querying.
        """
        index = self.data_objects[0].data.index
        for data_object in self.visible_data_objects[1:]:
            index = index.intersection(data_object.data.index)
        return index.tolist()

    def _reset_done(self):
        """Helper function to reset done flags.
        """
        self.recursive_counter = 0
        for data_id in self.id_to_data:
            self.done[data_id] = False

    def _recursive_apply(self, data_id, function, result):
        """A helper function to recursively apply function.

        Args:
            data_id: the id of data to apply the function.
            function: a function to apply to the data.
            result: a function to get return value for _recursive_apply.
        """
        if self.busy[data_id]:
            raise ValueError("Circular dependency detected.")

        data = self.id_to_data[data_id]
        if self.done[data_id]:
            return result(data)

        self.busy[data_id] = True
        dependencies = [self._recursive_apply(dep_id, function, result)
                        for dep_id in data.dependencies]
        function(data=data, dependencies=dependencies)
        self.busy[data_id] = False
        self.done[data_id] = True
        return result(data)

    def get_buffer(self):
        """Returns number of buffer days.
        """
        def result(data):
            return data.buffer

        def function(data, dependencies):
            self.recursive_counter += 1
            data.buffer_days(dependencies)

        self._reset_done()
        return max([self._recursive_apply(id_str, function, result) for id_str in self.id_to_data])

    def prepare_data(self):
        """Prepares all the data in the collection.
        """
        def result(data):
            return data

        def function(data, dependencies):
            if not data.ready:
                self.recursive_counter += 1
                data.prepare_data(self.from_date, self.to_date, self.stock_names, dependencies)

        if self.from_date is None or self.to_date is None:
            raise ValueError("Date range is not set-up.")

        self._reset_done()
        for id_str in self.id_to_data:
            self._recursive_apply(id_str, function, result)

    def reset(self):
        """Resets ressetable data objects.
        """
        def result(data):
            return data.ready

        def function(data, dependencies):
            self.recursive_counter += 1
            data.reset(dependencies)

        self._reset_done()
        for data_id in self.id_to_data:
            self._recursive_apply(data_id, function, result)

    def __getitem__(self, date):
        """Get the data for the date.

        Args:
            date: the specified lookup date.

        Returns:
            DataFrame row with the data.
        """
        return pd.concat([data_object[date] for data_object in self.visible_data_objects])
