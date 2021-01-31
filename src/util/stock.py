"""Utils for downloading stock data from the Quandl API.
"""
from os.path import join

import pandas as pd
import yfinance

from src.util.file import read_manifest_file, write_manifest_file
from src.util.file import read_csv_file, write_csv_file

DATA_PATH = "data"
STOCK_MANIFEST_FILE_NAME = "stock_data_manifest.json"

def get_stock_data(stock_names, from_date, to_date, path=DATA_PATH):
    """A function to get stock data.

    Args:
        stock_names: list of str with names of stocks.
        from_date: datetime start of the date range.
        to_date: datetime end  of the date range.
        path: path to manifest and saved stock data

    Returns:
        A pandas DataFrame with the stock information.
    """
    manifest_path = join(path, STOCK_MANIFEST_FILE_NAME)
    manifest = read_manifest_file(manifest_path)
    data_frames = [get_stock_data_for_single_stock(stock_name, from_date, to_date, manifest, path)
                   for stock_name in stock_names]
    data = pd.concat(data_frames, axis=1)
    write_manifest_file(manifest, manifest_path)
    return data

def get_stock_data_for_single_stock(stock_name, from_date, to_date, manifest, path=DATA_PATH):
    """A helper function to get stock data for a single stock.

    Args:
        stock_name: str with name of stock.
        from_date: datetime start of the date range.
        to_date: datetime end  of the date range.
        manifest: dict with the information about already downloaded stocks.
        path: path to manifest and saved stock data

    Returns:
        A pandas DataFrame with the stock information.
    """
    # pylint: disable=superfluous-parens
    if (stock_name in manifest
            and manifest[stock_name]["from_date"] <= from_date <= manifest[stock_name]["to_date"]
            and manifest[stock_name]["from_date"] <= to_date <= manifest[stock_name]["to_date"]):
        data = read_csv_file(join(path, "{}.csv".format(stock_name)))
        data = data.loc[from_date:to_date]
    else:
        start_date = from_date
        end_date = to_date
        if (stock_name in manifest):
            start_date = min(start_date, manifest[stock_name]["from_date"])
            end_date = max(end_date, manifest[stock_name]["to_date"])
        data = yfinance.download(stock_name, start_date, end_date, progress=False)
        data = data["Close"]
        data = data.rename(stock_name)
        manifest[stock_name] = {"from_date": from_date, "to_date": to_date}
        write_csv_file(data, join(path, "{}.csv".format(stock_name)))
    return data
