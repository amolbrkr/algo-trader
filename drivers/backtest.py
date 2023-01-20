import pandas as pd
from strategies.strategies import TestStrat
from backtesting import Backtest


TCS = pd.read_csv(
    f"hist_data/TCS_data.csv",
    delimiter=",",
    index_col="datetime",
    parse_dates=True,
)["2022-12-01 07:00:00":"2023-01-18 16:00:00"]

TCS = TCS[["open", "high", "low", "close", "volume"]]
TCS.columns = map(str.title, TCS.columns)


bt = Backtest(TCS, TestStrat, cash=10000, commission=0.002, exclusive_orders=True)

print(bt.run())
# bt.plot()
