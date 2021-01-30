"""Unit tests for data collection.
"""
import unittest

from parameterized import parameterized

from src.data import create_data_collection
from src.util import read_config_file


class TestDataCollection(unittest.TestCase):
    """Unit tests for data collection.
    """
    @parameterized.expand([
        ("test/duplicate_data_collection.yaml", ValueError),
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

    def test_catches_circular_dependency(self):
        """Checks if data collection catches circular dependency.
        """
        config = read_config_file("test/circular_dependency_data_collection.yaml")
        data_collection = create_data_collection(config)
        with self.assertRaises(ValueError):
            data_collection.prepare_data()

    def test_prepares_data(self):
        """Checks if data collection prepares the data properly.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        data_collection.prepare_data()
        for data in data_collection.data_objects:
            self.assertTrue(data.ready)

    def test_resets_data(self):
        """Checks if data collection prepares the data properly.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
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

    def test_getitem(self):
        """Checks if __getitem__ works as expected.
        """
        config = read_config_file("test/data_collection.yaml")
        data_collection = create_data_collection(config)
        self.assertFalse(data_collection[0])
