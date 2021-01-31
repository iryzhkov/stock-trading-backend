"""Class for running average analysis data.
"""
from src.data.stock_data_analysis import StockDataAnalysis


class RunningAverageAnalysis(StockDataAnalysis):
    """Class for running average analysis data.
    """
    name = "running_average_analysis"
    expected_num_dependencies = 1

    def __init__(self, dependencies=None, num_days=1):
        """Initializer for Running Average Analysis class

        Args:
            dependencies: a list of dependency ids for the data.
            num_days: number of days to take the average of.
        """
        super(RunningAverageAnalysis, self).__init__(dependencies)
        self.num_days = num_days
        self.id_str = "running_average_{}_for_{}".format(num_days, dependencies[0])

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """
        self.data = dependencies[0].data.rolling(self.num_days).mean()
        self.data.dropna(inplace=True)
        self.data = self.data.rename(lambda name: "ra_{}_{}".format(self.num_days, name), axis=1)
        self.ready = True

    def buffer_days(self, dependencies):
        """Figures out the buffer for the running average analysis.

        Args:
            dependencies: The list of buffer values for the dependencies.

        Returns:
            Number buffer days.
        """
        self.buffer = dependencies[0] + self.num_days
