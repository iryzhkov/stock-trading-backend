"""Base class for stock market agent.
"""
from abc import ABCMeta
from os.path import join

from stock_trading_backend.agent.model_factory import create_model
from stock_trading_backend.data import create_data_collection
from stock_trading_backend.simulation import create_reward
from stock_trading_backend.util import read_manifest_file, write_manifest_file

AGENT_PATH = "data/agent"
MODEL_PATH_TEMPLATE = join(AGENT_PATH, "{}.pkl")

class Agent(metaclass=ABCMeta):
    """Base class for stock market agent.
    """
    name = None
    requires_learning = False

    def __init__(self, data_collection_config, reward_config=None, model_config=None):
        """Initializer for Agent.

        Args:
            data_collection_config: configuration for the data collection used by the agent.
            reward_config: configuration for reward used by the agent.
            model_config: configuration for model used by the agent.
        """
        self.data_collection_config = data_collection_config
        self.stock_names = data_collection_config["stock_names"]
        self.reward_config = reward_config
        self.model_config = model_config
        self.id_str = self.name
        self.trained = False
        self.id_str_with_hash = None
        self._add_id_with_hash_values()

    def _add_id_with_hash_values(self):
        """Adds hash values to the id_str
        """
        data_collection = create_data_collection(self.data_collection_config)
        reward = None
        model = None
        if not self.reward_config is None:
            reward = create_reward(self.reward_config, None, None)
        if not self.model_config is None:
            model = create_model(self.model_config)
        self.id_str_with_hash = "{}_{}_{}_{}".format(self.id_str, hash(data_collection),
                                                     hash(reward), hash(model))

    @property
    def usable(self):
        """Returns true if the agent can be used for backtesting.
        """
        return not self.requires_learning or self.trained

    def extract_stock_feature(self, observation, feature_template=""):
        """Extracts stock feature from observation.

        Feature is expected to be: feature_template.format(stock_name)

        Args:
            observation: observation to extract feature from.
            feature_template: what the feature key looks like.
        """
        return [observation[feature_template.format(stock_name)] for stock_name in self.stock_names]

    def unpack_observation(self, observation):
        """Unpacks observation into: balance, net_worth, owned_stocks, stock_prices.

        Note:
            This is mostly usefull for non-reinforcement learning agents.

        Args:
            observation: pandas Series with observation data.

        Returns:
            balance, net worth, owned_stocks, stock_prices
        """
        balance = observation["balance"]
        net_worth = observation["net_worth"]
        stock_prices = self.extract_stock_feature(observation, "{}")
        owned_stocks = self.extract_stock_feature(observation, "owned_{}")
        return balance, net_worth, owned_stocks, stock_prices

    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def make_decision(self, observation, env, training=False):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
            training: boolean flag for specifying if this is training or testing.
            kwargs: other arguments passed to the function. Usually output of previous call.

        Returns:
            action: the action that agent decided to take.
            empty dict, since there is no additional information.
        """
        return env.action_space.sample(), {}

    def apply_learning(self, observations_batch, actions_batch, rewards_batch):
        """Applies learning for provided data.

        Args:
            observations_batch: a list of DataFrames with observations.
            actions_batch: a list of a list of actions.
            rewards_batch: a list of a list of rewards.

        Returns:
            Loss before training.
        """

    def can_be_loaded(self):
        """Checks if the agent can be loaded.
        """
        if not self.requires_learning:
            return True
        agent_manifest = read_manifest_file(join(AGENT_PATH, "manifest.json"))
        return self.id_str_with_hash in agent_manifest

    def save(self):
        """Saves the agent for future re-use.
        """
        if not self.requires_learning:
            return

        if not self.trained:
            raise ValueError("Agent must be trained before saving it.")

        manifest_path = join(AGENT_PATH, "manifest.json")
        model_path = join(MODEL_PATH_TEMPLATE.format(self.id_str_with_hash))
        agent_manifest = read_manifest_file(manifest_path)
        agent_manifest[self.id_str_with_hash] = {
            "trained": True
        }
        self.model.save(model_path)
        write_manifest_file(agent_manifest, manifest_path)

    def load(self):
        """Loads the saved version of the agent.
        """
        if not self.requires_learning:
            return

        path = join(AGENT_PATH, "manifest.json")
        agent_manifest = read_manifest_file(path)

        if self.id_str_with_hash not in agent_manifest:
            raise LookupError("Couldn't find the saved version.")

        model_path = join(MODEL_PATH_TEMPLATE.format(self.id_str_with_hash))
        self.model.load(model_path)
        self.trained = True
