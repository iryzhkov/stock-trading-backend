"""QLearning agent.
"""
from stock_trading_backend.agent.agent import Agent

class QLearningAgent(Agent):
    """Agent that uses Q-Learning strategy to figure out policy.
    """
    name = "q_learning_agent"
    requires_learning = True

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    def make_decision(self, observation, env, training=False):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
            training: boolean flag for specifying if this is training or testing.

        Returns:
            action: the action that agent decided to take.
        """
        return env.action_space.sample(), {}

    # pylint: disable=unused-argument
    def apply_learning(self, observations_batch, actions_batch, rewards_batch):
        """Applies learning for provided data.

        Args:
            observations_batch: a list of DataFrames with observations.
            actions_batch: a list of a list of actions.
            rewards_batch: a list of a list of rewards.

        Returns:
            Loss before training.
        """
        self.trained = True
