"""Class for running average analysis data.
"""
from src.data import StockDataAnalysis

class RunningAverageAnalysis(StockDataAnalysis):
    """Class for running average analysis data.
    """
    id = "running_{number_of_days}_average_analysis"
    is_stock_specific = True
