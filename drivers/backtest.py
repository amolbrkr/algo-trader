import pandas as pd
from utils.utils import Utils
from strategies.strategies import TestStrat
from backtesting import Backtest


TCS = Utils().read_data("TCS", "2022-12-01", "2023-01-18")
bt = Backtest(TCS, TestStrat, cash=10000, commission=0.002, exclusive_orders=True)

print(bt.run())
# bt.plot()
