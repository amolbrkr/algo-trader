import time
import pandas as pd
import backtrader as bt
from utils import Utils, Logger


class TestStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.ind.RSI(plot=False)
        self.price = self.data0.close
        self.scnt = self.fcnt = 0

    def next(self):
        if not self.position:
            if (
                self.rsi > 65
                and self.price[-2] > self.price[-1]
                and self.price[-1] > self.price[0]
            ):
                self.bp = self.price[0]
                print(f"Sell: {self.bp}")
                self.sell()
        else:
            sl = self.bp * 0.004 + self.bp
            tp = self.bp - self.bp * 0.012
            if self.price >= sl:
                print(f"Stop Loss: {self.price[0]}")
                self.fcnt += 1
                self.buy()

            if self.price <= tp:
                print(f"Take Profit: {self.price[0]}")
                self.scnt += 1
                self.buy()

    def stop(self):
        print(
            f"S: {self.scnt}, F: {self.fcnt}, Win%: {self.scnt / (self.scnt + self.fcnt) * 100}"
        )


if __name__ == "__main__":
    stock = "TCS"
    df = pd.read_csv(
        f"hist_data/{stock}_data.csv",
        delimiter=",",
        index_col="datetime",
        parse_dates=True,
    )

    # Get last year's data
    df = df["2023-01-01 07:00:00":"2023-01-17 07:00:00"]

    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(
        name=f"{stock} 5 Min", dataname=df, timeframe=bt.TimeFrame.Minutes
    )
    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.addstrategy(TestStrategy)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.plot(style="candlestick")
