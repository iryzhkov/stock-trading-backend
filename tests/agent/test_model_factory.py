"""Unit tests for model factory.
"""
import unittest

from parameterized import parameterized

from stock_trading_backend.agent import create_model, PolynomialModel
from stock_trading_backend.util import read_config_file


class TestModelFactory(unittest.TestCase):
    """Unit tests for model factory.
    """
    @parameterized.expand([
        ("model/linear.yaml", PolynomialModel),
    ])
    def test_creates_agent(self, config_filename, expected_class):
        """Checks if created model class is of the right class.

        Args:
            config_filename: the filename for the config file.
            expected_class: the expected class created from config file.
        """
        model = create_model(read_config_file(config_filename))
        self.assertIsInstance(model, expected_class)

    def test_lookup_error(self):
        """Checks if create agent raises lookup error.
        """
        with self.assertRaises(LookupError):
            _ = create_model({"name": "not_the_right_name"})
