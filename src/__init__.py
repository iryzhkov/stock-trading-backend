"""__init__.py for src sub-package
"""
from gym.envs.registration import register

register(
    id='stock-market-v0',
    entry_point='src.simulation:StockMarketSimulation'
)
