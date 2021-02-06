"""Training.
"""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import progressbar

from stock_trading_backend.simulation import StockMarketSimulation

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
def train_agent(agent, from_date=None, to_date=None, min_duration=60, max_duration=90, commission=0,
                max_stock_owned=1, min_start_balance=1000, max_start_balance=4000,
                stock_data_randomization=False, episode_batch_size=5, num_episodes=10):
    """Train an agent with provided params.

    Args:
        agent: the agent to train.
        from_date: datetime date for the start of the range.
        to_date: datetime date for the end of the range.
        min_duration: minimum length of the episode.
        max_duration: maximum length of the episode (if 0 will run for all available dates).
        max_stock_owned: a maximum number of different stocks that can be owned.
        commission: relative commission for each transcation.
        max_stock_owned: a maximum number of different stocks that can be owned.
        min_start_balance: the minimum starting balance.
        max_start_balance: the maximum starting balance.
        stock_data_randomization: whether to add stock data randomization.
        episode_batch_size: the number of episodes in a training batch.
        num_episodes: number of episodes that training going to last.
    """
    if not agent.requires_learning:
        raise ValueError("This agent does not need learning")

    if from_date is None or to_date is None:
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        from_date = today - timedelta(days=720)
        to_date = today - timedelta(days=60)

    simulation = StockMarketSimulation(agent.data_collection_config, from_date=from_date,
                                       to_date=to_date, min_start_balance=min_start_balance,
                                       max_start_balance=max_start_balance, commission=commission,
                                       max_stock_owned=max_stock_owned, min_duration=min_duration,
                                       max_duration=max_duration, reward_config=agent.reward_config,
                                       stock_data_randomization=stock_data_randomization)

    num_episodes_run = 0
    overall_reward_history = []
    loss_history = []

    observation = simulation.reset()
    _, kwargs = agent.make_decision(observation, simulation, False)
    kwargs_keys = kwargs.keys()
    batch_kwargs_keys = ["{}s_batch".format(key) for key in kwargs_keys]

    with progressbar.ProgressBar(max_value=num_episodes) as progress_bar:
        while num_episodes_run < num_episodes:
            batch_kwargs = {key: [] for key in batch_kwargs_keys}
            batch_rewards = []
            batch_observations = []
            batch_actions = []
            batch_reward = 0
            num_episodes_left_in_batch = episode_batch_size

            # Run the simulations in the batch.
            while num_episodes_left_in_batch > 0 and num_episodes_run < num_episodes:
                rewards = []
                actions = []
                kwargs = {key: [] for key in kwargs_keys}
                observation = simulation.reset()
                observations = pd.DataFrame(columns=observation.index)

                while not simulation.done:
                    action, _kwargs = agent.make_decision(observation, simulation, True)
                    observations = observations.append(observation, ignore_index=True)
                    actions.append(action)
                    for key in _kwargs:
                        kwargs[key].append(_kwargs[key])
                    observation, reward, _ = simulation.step(action)
                    rewards.append(reward)

                overall_reward = simulation.overall_reward
                batch_reward += overall_reward
                rewards = np.asarray(rewards) + overall_reward
                batch_rewards.append(rewards)
                batch_observations.append(observations)
                batch_actions.append(actions)
                for key in kwargs:
                    batch_kwargs["{}s_batch".format(key)].append(kwargs[key])
                num_episodes_run += 1
                num_episodes_left_in_batch -= 1
                progress_bar.update(num_episodes_run)

            # Utilize data from the simulations to train agents.
            loss = agent.apply_learning(batch_observations, batch_actions, batch_rewards,
                                        **batch_kwargs)

            overall_reward_history += [batch_reward / episode_batch_size]
            loss_history.append(loss)

    return overall_reward_history, loss_history
