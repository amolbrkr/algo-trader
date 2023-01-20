import pandas as pd
from strategies.strategies import TestStrat
from backtesting import Backtest


class BTPYDriver:
    def __init__(self, data, strategy, **kwargs):
        self.test = Backtest(data, strategy, **kwargs)
