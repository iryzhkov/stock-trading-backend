"""Factory functions for data classes.
"""
from src.data.data_collection import DataCollection
from src.data.generated_stock_data import GeneratedStockData
from src.data.randomized_stock_data import RandomizedStockData
from src.data.real_stock_data import RealStockData
from src.data.running_average_analysis import RunningAverageAnalysis


DATA_CLASSES = [
    GeneratedStockData,
    RandomizedStockData,
    RealStockData,
    RunningAverageAnalysis,
]
DATA_NAME_MAPPING = {data.name:data for data in DATA_CLASSES}

def create_data(data_config):
    """Factory for Data classes.

    Args:
        data_config: dictionary with the configuration for the Data class.
    """
    if data_config["name"] not in DATA_NAME_MAPPING:
        raise LookupError("There is no Data with the {} name.".format(data_config["name"]))
    data_class_name = data_config["name"]
    del data_config["name"]
    return DATA_NAME_MAPPING[data_class_name](**data_config)

def create_data_collection(data_collection_config):
    """Factory for Data Collection.

    Args:
        data_collection_config: dictionary with the configuration for the Data Collection class.
    """
    data_configs = data_collection_config["data"]
    data_objects = [create_data(config) for config in data_configs]
    del data_collection_config["data"]
    return DataCollection(data_objects, **data_collection_config)
