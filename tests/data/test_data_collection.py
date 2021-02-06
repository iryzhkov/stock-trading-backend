"""Unit tests for data collection.
"""
from datetime import datetime

import unittest

from parameterized import parameterized

from stock_trading_backend.data import create_data_collection, RealStockData
from stock_trading_backend.util import read_config_file


class TestDataCollection(unittest.TestCase):
    """Unit tests for data collection.
    """
    @parameterized.expand([
        ("test/missing_dependency_data_collection.yaml", LookupError),
        ("test/no_stock_data_collection.yaml", ValueError),
    ])
    def test_catches_config_error(self, config_filename, excpecetd_exception):
        """Checks if data collection catches configuration errors.

        Args:
            config_filename: the filename for the config file.
            excpecetd_exception: the expected exception.
        """
        with self.assertRaises(excpecetd_exception):
            create_data_collection(read_config_file(config_filename))

    def test_ignores_duplicates(self):
        """Checks if data collection ignores duplicates.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        stock_data = RealStockData()
        returned_stock_data = data_collection.append(stock_data)
        self.assertIsInstance(returned_stock_data, RealStockData)
        self.assertNotEqual(stock_data, returned_stock_data)

    def test_catches_circular_dependency(self):
        """Checks if data collection catches circular dependency.
        """
        config = read_config_file("test/circular_dependency_data_collection.yaml")
        data_collection = create_data_collection(config)
        with self.assertRaises(ValueError):
            data_collection.reset()

    def test_adds_randomization(self):
        """Checks if data collection adds randomization properly.
        """
        config = read_config_file("test/data_collection.yaml")
        config["stock_data_randomization"] = True
        data_collection = create_data_collection(config)
        self.assertEqual(3, len(data_collection.data_objects))

        config = read_config_file("test/simulation.yaml")
        config["stock_data_randomization"] = False
        data_collection = create_data_collection(config)
        self.assertEqual(1, len(data_collection.data_objects))

        config = read_config_file("test/simulation.yaml")
        config["stock_data_randomization"] = True
        data_collection = create_data_collection(config)
        self.assertEqual(2, len(data_collection.data_objects))
        randomization_layer = data_collection.data_objects[0]
        stock_data = data_collection.data_objects[1]
        self.assertEqual(randomization_layer.dependencies[0], stock_data.id_str)

    def test_use_relative(self):
        """Checks if data collection uses relative stock data properly.
        """
        config = read_config_file("test/data_collection.yaml")
        config["use_relative_stock_data"] = True
        data_collection = create_data_collection(config)
        self.assertEqual(4, len(data_collection.data_objects))
        self.assertNotEqual(data_collection.stock_data_id, data_collection.absolute_stock_data_id)

    def test_prepares_data(self):
        """Checks if data collection prepares the data properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        self.assertEqual(data_collection.stock_data_id, data_collection.absolute_stock_data_id)
        data_collection.set_date_range(from_date, to_date)
        data_collection.prepare_data()
        for data in data_collection.data_objects:
            self.assertTrue(data.ready)

    def test_checks_date_range_set(self):
        """Checks if data collection catches when date range is not set.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        with self.assertRaises(ValueError):
            data_collection.prepare_data()

    def test_resets_data(self):
        """Checks if data collection prepares the data properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        data_collection.set_date_range(from_date, to_date)
        data_collection.prepare_data()
        for data in data_collection.data_objects:
            self.assertTrue(data.ready)
        self.assertEqual(3, data_collection.recursive_counter)
        data_collection.reset()
        for data in data_collection.data_objects:
            if data.name != "real_stock_data":
                self.assertFalse(data.ready)
            else:
                self.assertTrue(data.ready)
        data_collection.prepare_data()
        self.assertEqual(2, data_collection.recursive_counter)

    def test_get_buffer(self):
        """Checks if buffer days is calculated correctly.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        self.assertEqual(10, data_collection.get_buffer())

    def test_get_availbale_dates(self):
        """Checks if get available dates works properly.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        data_collection.set_date_range(from_date, to_date)
        data_collection.prepare_data()
        available_dates = data_collection.get_available_dates()
        self.assertEqual(10, len(available_dates))

    def test_getitem(self):
        """Checks if __getitem__ works as expected.
        """
        expected_index = ["GOOG", "AMZN", "ra_10_stock_data_GOOG", "ra_10_stock_data_AMZN"]
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        data_collection.set_date_range(from_date, to_date)
        data_collection.prepare_data()
        available_dates = data_collection.get_available_dates()
        self.assertTrue((expected_index == data_collection[available_dates[0]].index.tolist()))

    def test_hash(self):
        """Checks if __hash__ works.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        self.assertIsNotNone(hash(data_collection))
