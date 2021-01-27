"""Class for running average analysis data.
"""
from src.data import StockDataAnalysis


class RunningAverageAnalysis(StockDataAnalysis):
    """Class for running average analysis data.
    """
    id = "running_{number_of_days}_average_analysis"
    is_stock_specific = True

    def pre_run(self):
        """Stuff to run before.
        """

    def reset(self):
        """Stuff to run
        """
