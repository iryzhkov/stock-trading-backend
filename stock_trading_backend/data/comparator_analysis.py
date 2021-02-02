"""Class for comparator analysis.
"""
from stock_trading_backend.data.stock_data_analysis import StockDataAnalysis

OPERATORS = ["gt", "ge", "lt", "le", "eq", "ne"]


class ComparatorAnalysis(StockDataAnalysis):
    """Class for comparator analysis.

    Compares two dependencies element-wise.
    """
    name = "comparator"
    expected_num_dependencies = 2

    def __init__(self, dependencies=None, visible=True, operator="gt"):
        """Initializer for Greater Than Analysis class

        Args:
            dependencies: a list of dependency ids for the data.
            visible: whether the data is visible in data_collection[date].
        """
        super(ComparatorAnalysis, self).__init__(dependencies, visible)
        if operator not in OPERATORS:
            raise ValueError("Operator {} is not allowed".format(operator))
        self.operator = operator
        self.id_str = "{}_{}_{}".format(dependencies[0], operator, dependencies[1])
        self.feature_template = self.id_str + "_{}"

    def prepare_data(self, from_date, to_date, stock_names, dependencies):
        """Data preparation.

        Gets the data prepared.

        Args:
            from_date: datetime start of the date range.
            to_date: datetime end of the date range.
            stock_names: a list of stock names to prepare.
            dependencies: a list of prepared data dependencies.
        """
        exec_str = "dependencies[0].data.{}(dependencies[1].data).dropna()".format(self.operator)
        # pylint: disable=eval-used
        self.data = eval(exec_str)
        self.data = self.data.astype("int32")
        self.data.columns = [self.feature_template.format(name) for name in stock_names]
        self.ready = True
