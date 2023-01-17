import pandas as pd
import backtrader as bt


class VolumeWeightedAveragePrice(bt.Indicator):
    plotinfo = dict(subplot=False)

    params = (("period", 30),)

    alias = (
        "VWAP",
        "VolumeWeightedAveragePrice",
    )
    lines = ("VWAP",)
    plotlines = dict(VWAP=dict(alpha=0.50, linestyle="-.", linewidth=2.0))

    def __init__(self):
        # Before super to ensure mixins (right-hand side in subclassing)
        # can see the assignment operation and operate on the line
        cumvol = bt.ind.SumN(self.data.volume, period=self.p.period)
        typprice = (
            (self.data.close + self.data.high + self.data.low) / 3
        ) * self.data.volume
        cumtypprice = bt.ind.SumN(typprice, period=self.p.period)
        self.lines[0] = cumtypprice / cumvol

        super(VolumeWeightedAveragePrice, self).__init__()


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        price = self.data
        ema = bt.ind.EMA(period=50)
        self.rsi = bt.ind.RSI(period=2, safediv=True)
        self.crossover = bt.ind.CrossOver(price, ema)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, %.2f" % order.executed.price)
            elif order.issell():
                self.log("SELL EXECUTED, %.2f" % order.executed.price)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None


class HighVolStrat(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, %.2f" % order.executed.price)
            elif order.issell():
                self.log("SELL EXECUTED, %.2f" % order.executed.price)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])
        if self.order:
            return

        if not self.position:
            if (
                self.dataclose[0] > self.dataclose[-1]
                and self.dataclose[-1] > self.dataclose[-2]
                and self.dataclose[-2] > self.dataclose[-3]
            ):
                self.enter_point = len(self)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()
        else:
            if len(self) > (self.enter_point + 10):
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()


if __name__ == "__main__":
    df = pd.read_csv(
        "hist_data/TCS_data.csv", delimiter=",", index_col="datetime", parse_dates=True
    )

    # Get last year's data
    df = df["2021-01-01 07:00:00":"2023-01-17 07:00:00"]

    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(
        name="TCS 5 Min", dataname=df, timeframe=bt.TimeFrame.Minutes
    )
    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.addstrategy(HighVolStrat)
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.plot(style="candlestick")
