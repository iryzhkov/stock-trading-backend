"""Demonstration of how to use the API.
"""
import matplotlib
import matplotlib.pyplot as plt

from stock_trading_backend import api, train, backtest

agent = api.get_agent_object("sarsa_learning_agent_1", "generated_1",
                             "net_worth_ratio", "neural_network")
reward_history, loss_history = train.train_agent(agent, episode_batch_size=5, num_episodes=10)

fig, axs =  plt.subplots(2, figsize=(10, 10))
axs[0].plot(reward_history)
axs[0].plot([-1, len(reward_history)], [0, 0], 'r--')
axs[0].set_title("Reward history vs batch number")

axs[1].plot(loss_history)
axs[1].set_title("Loss history vs batch number")
axs[1].set_yscale("log")
plt.savefig("demo_training.png")

backtest_output = backtest.backtest_agent(agent)
num_stocks = len(agent.stock_names)
fix, axs = plt.subplots(num_stocks + 1, figsize=(10, 15))
axs[0].plot(backtest_output["net_worth_history"], label="net_worth")
axs[0].plot(backtest_output["balance_history"], label="balance")
axs[0].legend()

for stock_id in range(num_stocks):
    axs[stock_id + 1].plot(backtest_output["stocks_price_history"][:,stock_id])
    axs[stock_id + 1].set_title(backtest_output["stock_names"][stock_id])

def add_action(e, stock_id, action):
    if action == 0:
        return
    colors = {1: "blue", -1: "magenta"}
    axs[stock_id + 1].plot([e, e], [0, backtest_output["stocks_price_history"][e][stock_id]],
                           "--", color=colors[action])

for episode, actions in enumerate(backtest_output["action_history"]):
    for stock_id, action in enumerate(actions):
        add_action(episode, stock_id, action)

plt.savefig("demo_backtesting.png")
