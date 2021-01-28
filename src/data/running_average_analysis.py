"""Class for running average analysis data.
"""
from src.data.stock_data_analysis import StockDataAnalysis


class RunningAverageAnalysis(StockDataAnalysis):
    """Class for running average analysis data.
    """
    name = "running_average_analysis"
    is_stock_specific = True

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
