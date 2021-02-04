"""Unit tests for agent factory.
"""
import unittest

from parameterized import parameterized

from stock_trading_backend.agent import create_agent, FollowingFeatureAgent
from stock_trading_backend.util import read_config_file


class TestAgentFactory(unittest.TestCase):
    """Unit tests for agent factory.
    """
    @parameterized.expand([
        ("agent/following_feature_agent_1.yaml", FollowingFeatureAgent),
    ])
    def test_creates_agent(self, config_filename, expected_class):
        """Checks if created agent class is of the right class.

        Args:
            config_filename: the filename for the config file.
            expected_class: the expected class created from config file.
        """
        data_collection_config = read_config_file("data/default.yaml")
        agent = create_agent(read_config_file(config_filename), data_collection_config, None)
        self.assertIsInstance(agent, expected_class)

    def test_lookup_error(self):
        """Checks if create agent raises lookup error.
        """
        with self.assertRaises(LookupError):
            _ = create_agent({"name": "not_the_right_name"}, None, None)
