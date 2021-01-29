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
