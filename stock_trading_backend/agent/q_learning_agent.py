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
        """
        return env.action_space.sample()

    def apply_learning(self, observations, actions, rewards):
        """Applies learning for provided data.

        Args:
            observations: DataFrame with observations.
            actions: a list of actions.
            rewards: a list of rewards.

        Returns:
            Loss after training.
        """
        self.trained = True
