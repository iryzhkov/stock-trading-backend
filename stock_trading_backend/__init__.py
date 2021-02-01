"""__init__.py for stock_trading_backend sub-package
"""
from gym.envs.registration import register

register(
    id='stock-market-v0',
    entry_point='stock_trading_backend.simulation:StockMarketSimulation'
)
