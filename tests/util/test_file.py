"""Unit tests for file utils.
"""
from datetime import datetime

import os
import unittest
import pandas as pd

from stock_trading_backend.util import read_config_file, FileSourceType, read_manifest_file
from stock_trading_backend.util import read_csv_file, write_csv_file, write_manifest_file


class TestFileUtilsData(unittest.TestCase):
    """Unit tests for file utils.
    """
    def test_config_reader(self):
        """Unit test for config reader.
        """
        config = read_config_file("test/test_config.yaml")
        self.assertEqual(type({}), type(config))
        self.assertIn("test", config)
        self.assertEqual("test", config["test"])

    def test_not_implemented(self):
        """Test not-implemented features.
        """
        with self.assertRaises(NotImplementedError):
            _ = read_config_file("test/test_config.yaml", FileSourceType.aws)

        with self.assertRaises(NotImplementedError):
            _ = read_manifest_file("data/test/test_manifest.json", FileSourceType.aws)

        with self.assertRaises(NotImplementedError):
            write_manifest_file({}, "data/test/test_manifest.json", FileSourceType.aws)

        with self.assertRaises(NotImplementedError):
            _ = read_csv_file("data/test/test.csv", FileSourceType.aws)

        with self.assertRaises(NotImplementedError):
            write_csv_file(pd.DataFrame(), "data/test/test.csv", FileSourceType.aws)

    def test_read_manifest(self):
        """Test for manifest reader.
        """
        manifest = read_manifest_file("data/test/test_manifest.json")
        self.assertEqual(type({}), type(manifest))
        self.assertIn("stock", manifest)
        self.assertEqual("test", manifest["stock"])

    def test_read_new_manifest(self):
        """Test for manifest reader for non-existent manifest.
        """
        manifest = read_manifest_file("data/test/non_existent.json")
        self.assertEqual(type({}), type(manifest))
        self.assertEqual(0, len(manifest))

    def test_manifest_works_with_dates(self):
        """Test for manifest reader and writer for dates.
        """
        file_path = "data/test/write_test.json"
        date = datetime(2015, 1, 1)
        manifest = {"stock_date": date}
        write_manifest_file(manifest, file_path)
        manifest = read_manifest_file(file_path)
        os.remove(file_path)
        self.assertIn("stock_date", manifest)
        self.assertEqual(date, manifest["stock_date"])

    def test_write_new_manifest(self):
        """Test for manifest writer for non-existent manifest.
        """
        file_path = "data/test/write_test.json"
        manifest = {"stock": "write_test"}
        write_manifest_file(manifest, file_path)
        manifest = read_manifest_file(file_path)
        os.remove(file_path)
        self.assertIn("stock", manifest)
        self.assertEqual("write_test", manifest["stock"])

    def test_read_csv_file(self):
        """Test for csv reader.
        """
        data_frame = read_csv_file("data/test/test.csv")
        self.assertIsInstance(data_frame, pd.DataFrame)
        self.assertEqual("test", data_frame.loc[0].item())

    def test_write_csv_file(self):
        """Test for csv reader.
        """
        file_path = "data/test/write_test.json"
        data_frame = pd.DataFrame(["write_test"])
        write_csv_file(data_frame, file_path)
        data_frame = read_csv_file(file_path)
        os.remove(file_path)
        self.assertIsInstance(data_frame, pd.DataFrame)
        self.assertEqual("write_test", data_frame.loc[0].item())
