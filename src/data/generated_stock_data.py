"""Class for storing generated stock data.
"""
# pylint: disable=unused-import
import math

from datetime import datetime

import numpy as np
import pandas as pd

from src.data.stock_data import StockData


# pylint: disable=too-few-public-methods
class GeneratedStockData(StockData):
    """Class for storing generated stock data.
    """
    name = "generated_stock_data"

    def __init__(self, dependencies=None, evaluation_functions=None):
        """Initializer for Generated Stock Data class

        Args:
            dependencies: a list of dependency ids for the data.

        """
        super(GeneratedStockData, self).__init__(dependencies)
        if not evaluation_functions:
            raise ValueError("No evaluation functions provided.")
        self.evaluation_functions = evaluation_functions
        self.anchor_date = datetime(2010, 1, 1)

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """
        anchor_date = datetime(2010, 1, 1)
        num_days = (to_date - from_date).days + 1
        diff = from_date - anchor_date if from_date > anchor_date else anchor_date - from_date
        diff = diff.days
        array = np.zeros((num_days, len(stock_names)))
        for day_index in range(num_days):
            for stock_index in range(len(stock_names)):
                evaluation_function_index = stock_index % len(self.evaluation_functions)
                evaluation_function = self.evaluation_functions[evaluation_function_index]
                # pylint: disable=eval-used
                array[day_index][stock_index] = eval(evaluation_function)
            diff += 1
        index = pd.Index(pd.date_range(from_date, to_date))
        self.data = pd.DataFrame(array, index=index, columns=stock_names)
        self.ready = True
