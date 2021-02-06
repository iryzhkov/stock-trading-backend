"""Factory function for reward.
"""
from copy import deepcopy

from stock_trading_backend.agent.polynomial_model import PolynomialModel
from stock_trading_backend.agent.neural_network_model import NeuralNetworkModel

MODEL_CLASSES = [
    PolynomialModel,
    NeuralNetworkModel,
]
MODEL_NAME_MAPPING = {model.name:model for model in MODEL_CLASSES}

def create_model(model_config):
    """Factory for model objects.

    Args:
        model_config: config for model.
    """
    if model_config["name"] not in MODEL_NAME_MAPPING:
        raise LookupError("Model of type {} is not found.".format(model_config["name"]))
    model_config = deepcopy(model_config)
    model_name = model_config["name"]
    del model_config["name"]
    return MODEL_NAME_MAPPING[model_name](**model_config)
