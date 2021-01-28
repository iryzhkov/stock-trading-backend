"""Class for running average analysis data.
"""
from src.data.stock_data_analysis import StockDataAnalysis


class RunningAverageAnalysis(StockDataAnalysis):
    """Class for running average analysis data.
    """
    name = "running_average_analysis"
    is_stock_specific = True

    def __init__(self, dependencies=None, num_days=1):
        """Initializer for Running Average Analysis class

        Args:
            dependencies: a list of dependency ids for the data.
            num_days: number of days to take the average of.
        """
        super(RunningAverageAnalysis, self).__init__(dependencies)
        self.num_days = num_days

    def prepare_data(self, date_range, stock_names, dependencies):
        """Data preparation for running average analysis.

        Gets the data prepared.

        Args:
            date_range: a tuple of dates that provides a range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared dependencies.
        """
        self.ready = True

    def reset(self):
        """Stuff to run
        """
