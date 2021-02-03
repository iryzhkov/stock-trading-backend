"""QLearning agent.
"""
from stock_trading_backend.agent.agent import Agent

class QLearningAgent(Agent):
    """Agent that uses Q-Learning strategy to figure out policy.
    """
    name = "q_learning_agent"
    requires_learning = True

    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def make_decision(self, observation, env):
        """Make decision based on the given data.

        Args:
            observation: current state of the environment.
            env: the gym environment.
        """
        return env.action_space.sample()

    def apply_learning(self):
        """Applies learning for provided data.
        """
        self.trained = True
