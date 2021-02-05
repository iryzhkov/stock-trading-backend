"""Demonstration of how to use the API.
"""
import matplotlib
import matplotlib.pyplot as plt

from stock_trading_backend import api, train, backtest

agent = api.get_agent_object("sarsa_learning_agent_1", "generated_1",
                             "net_worth_ratio", "linear")
reward_history, loss_history = train.train_agent(agent, episode_batch_size=10, num_episodes=100)

fig, axs =  plt.subplots(2, figsize=(10, 10))
axs[0].plot(reward_history)
axs[0].set_title("Reward history vs batch number")
axs[1].plot(loss_history)
axs[1].set_title("Loss history vs batch number")
axs[1].set_yscale("log")
plt.savefig("demo_training.png")

#print(reward_history)
#print(loss_history)
