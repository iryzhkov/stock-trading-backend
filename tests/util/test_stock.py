"""Unit tests for stock utils.
"""
import os
import unittest

from datetime import datetime

import pandas as pd

from stock_trading_backend.util import write_manifest_file, read_manifest_file, write_csv_file
from stock_trading_backend.util import get_stock_data, get_stock_data_for_single_stock, STOCK_MANIFEST_FILE_NAME

class TestFileUtilsData(unittest.TestCase):
    """Unit tests for stock utils.
    """
    def clean_csv_files(self, path, stock_names):
        """Helper function to clean csv files after test.
        """
        for stock_name in stock_names:
            file_path = os.path.join(path, "{}.csv".format(stock_name))
            self.assertTrue(os.path.exists(file_path))
            os.remove(file_path)

    def test_stock_data_for_single_stock(self):
        """Unit test for getting single stock data.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_name = "GOOG"
        manifest = {}
        path = "data/test"

        data = get_stock_data_for_single_stock(stock_name, from_date, to_date, manifest, path)
        self.clean_csv_files(path, [stock_name])

        self.assertEqual(19, len(data))
        self.assertEqual("GOOG", data.name)

    def test_stock_data_for_single_stock_read_from_csv(self):
        """Unit test for getting single stock data reading from csv.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_name = "GOOG"
        path = "data/test"
        manifest = {stock_name: {"from_date": from_date, "to_date": to_date}}

        data_frame = pd.DataFrame(["test"], pd.date_range(from_date, from_date))
        data_frame.index.name = "Date"
        write_csv_file(data_frame, os.path.join(path, "{}.csv".format(stock_name)))

        data = get_stock_data_for_single_stock(stock_name, from_date, to_date, manifest, path)
        self.clean_csv_files(path, [stock_name])

        self.assertEqual("test", data.iloc[0].item())

    def test_stock_data_for_single_stock_partial_manifest(self):
        """Unit test for getting single stock data reading from csv.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_name = "GOOG"
        path = "data/test"
        manifest = {stock_name: {"from_date": from_date, "to_date": from_date}}

        data = get_stock_data_for_single_stock(stock_name, from_date, to_date, manifest, path)
        self.clean_csv_files(path, [stock_name])

        self.assertEqual(19, len(data))
        self.assertEqual("GOOG", data.name)

    def test_stock_data_for_multiple_stock(self):
        """Unit test for getting stock data.
        """
        from_date = datetime(2016, 1, 1)
        to_date = datetime(2016, 2, 1)
        stock_names = ["GOOG", "TSLA"]
        path = "data/test"

        write_manifest_file({}, os.path.join(path, STOCK_MANIFEST_FILE_NAME))
        data = get_stock_data(stock_names, from_date, to_date, path)
        self.clean_csv_files(path, stock_names)
        manifest = read_manifest_file(os.path.join(path, STOCK_MANIFEST_FILE_NAME))
        write_manifest_file({}, os.path.join(path, STOCK_MANIFEST_FILE_NAME))

        for stock_name in stock_names:
            self.assertIn(stock_name, manifest)
        self.assertTrue((stock_names == data.columns.tolist()))
