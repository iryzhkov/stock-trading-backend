"""SARSA Learning agent class.
"""
import random

import numpy as np
import pandas as pd

from stock_trading_backend.agent.agent import Agent
from stock_trading_backend.agent.model_factory import create_model

# pylint: disable=too-many-arguments
class SARSALearningAgent(Agent):
    """Agent that uses SARSA-Learning strategy to figure out policy.
    """
    name = "sarsa_learning_agent"
    requires_learning = True

    def __init__(self, data_collection_config, reward_config=None, model_config=None,
                 discount_factor=0.1, epsilon=0.1, learning_rate=0.1, num_epochs=5,
                 initial_num_epochs=50):
        """Initializer for FollowingFeatureAgent class.

        Args:
            data_collection_config: configuration for the data collection used by the agent.
            reward_config: configuration for reward used by the agent.
            model_config: configuration for model used by the agent.
            discount_factor: discount factor.
            epsilon: epsilon value for epsilon-greedy exploration strategy.
            learning_rate: learning rate of the agent.
            num_epochs: number of epochs to run for each apply_learning.
            initial_num_epochs: number of epochs to run on the first apply_learning.
        """
        super(SARSALearningAgent, self).__init__(data_collection_config, reward_config,
                                                 model_config)
        if model_config is None:
            raise ValueError("Learning agents require model.")
        self.model = create_model(model_config)
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.initial_num_epochs = initial_num_epochs

    # pylint: disable=unused-argument
    def make_decision(self, observation, env, training=False):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
            training: boolean flag for specifying if this is training or testing.
        """
        possible_actions = list(env.action_space_generator())
        if random.random() < self.epsilon: # pragma: no cover
            return random.choice(possible_actions)

        state_action_values = self.model.predict(observation, possible_actions)
        return possible_actions[np.argmax(state_action_values)]

    # pylint: disable=too-many-locals
    def apply_learning(self, observations_batch, actions_batch, rewards_batch):
        """Applies learning for provided data.

        Args:
            observations_batch: a list of DataFrames with observations.
            actions_batch: a list of a list of actions.
            rewards_batch: a list of a list of rewards.

        Returns:
            Loss before training.
        """
        _observations = pd.DataFrame(columns=observations_batch[0].columns)
        _actions = []
        _expected_values = []

        # Unpack episodes in a batch
        for observations, actions, rewards in zip(observations_batch, actions_batch, rewards_batch):
            q_values = self.model.predict_with_multiple_observations(observations, actions).tolist()

            def calculate_expected_value(i):
                result = q_values[i] * (1 - self.learning_rate)
                result += self.learning_rate * (rewards[i] + q_values[i+1] * self.discount_factor)
                return result

            if self.trained:
                expected_values = list(map(calculate_expected_value, range(len(actions) - 1)))
                _observations = _observations.append(observations.iloc[:-1], ignore_index=True)
                _actions += actions[:-1]
                num_epochs = self.num_epochs
            else:
                # Model's initial estimations are random, so use rewards for first pass.
                expected_values = rewards
                _observations = _observations.append(observations, ignore_index=True)
                _actions += actions
                num_epochs = self.initial_num_epochs

            _expected_values.extend(expected_values)

        losses = []

        # pylint: disable=unused-variable
        for i in range(num_epochs):
            losses.append(self.model.train(_observations, _actions, _expected_values))

        self.trained = True
        return losses[0]
