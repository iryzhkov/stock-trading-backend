"""SARSA Learning agent class.
"""
import random

import numpy as np

from stock_trading_backend.agent.agent import Agent
from stock_trading_backend.agent.model_factory import create_model

# pylint: disable=too-many-arguments
class SARSALearningAgent(Agent):
    """Agent that uses SARSA-Learning strategy to figure out policy.
    """
    name = "sarsa_learning_agent"
    requires_learning = True

    def __init__(self, data_collection_config, reward_config=None, model_config=None,
                 discount_factor=0.1, epsilon=0.1, num_epochs=20):
        """Initializer for FollowingFeatureAgent class.

        Args:
            data_collection_config: configuration for the data collection used by the agent.
            reward_config: configuration for reward used by the agent.
            model_config: configuration for model used by the agent.
            discount_factor: discount factor.
            epsilon: epsilon value for epsilon-greedy exploration strategy.
            num_epochs: number of epochs to run for each apply_learning.
        """
        super(SARSALearningAgent, self).__init__(data_collection_config, reward_config,
                                                 model_config)
        if model_config is None:
            raise ValueError("Learning agents require model.")
        self.model = create_model(model_config)
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.num_epochs = num_epochs

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

    def apply_learning(self, observations, actions, rewards):
        """Applies learning for provided data.

        Args:
            observations: DataFrame with observations.
            actions: a list of actions.
            rewards: a list of rewards.

        Returns:
            Loss after training.
        """
        observations = observations.iloc[:-1]
        actions = actions[:-1]
        # pylint: disable=unused-variable
        for i in range(self.num_epochs):
            q_values = self.model.predict_with_multiple_observations(observations, actions).tolist()
            expected_values = [r + q_v[0] * self.discount_factor
                               for r, q_v in zip(rewards[:-1], q_values[1:])]
            loss = self.model.train(observations, actions, expected_values)
        self.trained = True
        return loss
