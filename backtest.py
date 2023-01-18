import time
import pytz
import pandas as pd
import backtrader as bt
from datetime import datetime, time
from utils import Utils, Logger


class EMAStrat(bt.Strategy):
    def __init__(self):
        ema1 = bt.ind.EMA(period=5)
        self.ema2 = bt.ind.EMA(period=10)
        self.crossover = bt.ind.CrossOver(ema1, self.ema2, plot=False)
        self.price = self.data0.close
        self.scnt = self.fcnt = 0

    def next(self):
        if not self.position:
            if self.price[0] > self.ema2[0] and self.crossover > 0:
                self.bp = self.price[0]
                print(f"Buy: {self.bp}")
                self.buy()
        else:
            sl = self.bp - 0.004 * self.bp
            tp = self.bp + 0.012 * self.bp

            if self.price <= sl:
                print(f"Stop Loss: {self.price[0]}")
                self.fcnt += 1
                self.sell()

            if self.price >= tp:
                print(f"Take Profit: {self.price[0]}")
                self.scnt += 1
                self.sell()

    def stop(self):
        print(
            f"S: {self.scnt}, F: {self.fcnt}, Win%: {self.scnt / (self.scnt + self.fcnt) * 100}"
        )


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
        name=f"{stock} 5 Min",
        dataname=df,
        timeframe=bt.TimeFrame.Minutes,
        fromdate=datetime(2023, 1, 1),
        todate=datetime(2023, 1, 17),
        sessionstart=time(9, 5),
        sessionend=time(15, 25),
        tz=pytz.timezone("Asia/Kolkata"),
    )
    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.broker.set_coc(True)
    cerebro.addstrategy(EMAStrat)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.plot(style="candlestick")
