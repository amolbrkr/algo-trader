import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA

TCS = pd.read_csv(
    f"hist_data/TCS_data.csv",
    delimiter=",",
    index_col="datetime",
    parse_dates=True,
)["2023-01-01 07:00:00":"2023-01-18 16:00:00"]

TCS = TCS[["open", "high", "low", "close", "volume"]]
TCS.columns = map(str.title, TCS.columns)


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


bt = Backtest(TCS, SmaCross, cash=10000, commission=0.002, exclusive_orders=True)

output = bt.run()
bt.plot()
