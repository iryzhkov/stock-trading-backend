"""Class for storing relative.
"""
from stock_trading_backend.data.stock_data import StockData


class RelativeStockData(StockData):
    """Class for storing relative stock data.

    Instad of actual stock price it stores how much it shanged from previous day.

    For example: [100, 200, 200, 100] -> [1, 0, -0.5]
    """
    name = "relative_stock_data"
    expected_num_dependencies = 1

    def __init__(self, dependencies=None, visible=False, scaling_factor=1):
        """Initializer for relative stock data class

        Args:
            dependencies: a list of dependency ids for the data.
            visible: whether the data is visible in data_collection[date].
            scaling_factor: multiply the output by this.
        """
        super(RelativeStockData, self).__init__(dependencies, visible)
        self.id_str = "relative_{}".format(self.dependencies[0])
        self.scaling_factor = scaling_factor

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """
        other_data = dependencies[0].data
        self.data = (other_data.diff(1) / other_data.shift(1)).dropna() * self.scaling_factor
        self.ready = True

    def buffer_days(self, dependencies):
        """Figures out the buffer for the running average analysis.

        Args:
            dependencies: The list of buffer values for the dependencies.

        Returns:
            Number buffer days.
        """
        self.buffer = dependencies[0] + 1
