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
        cumvol = bt.ind.SumN(self.data.volume, period=self.p.period)
        typprice = (
            (self.data.close + self.data.high + self.data.low) / 3
        ) * self.data.volume
        cumtypprice = bt.ind.SumN(typprice, period=self.p.period)
        self.lines[0] = cumtypprice / cumvol
        super(VolumeWeightedAveragePrice, self).__init__()


class Logger:
    def __init__(self, datas) -> None:
        self.datas = datas

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")


class Utils:
    def __init__(self):
        pass

    def notify_order(self, obj, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                obj.log(f"BUY EXECUTED, {order.executed.price}")
            elif order.issell():
                obj.log(f"SELL EXECUTED, {order.executed.price}")
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            obj.log("Order Canceled/Margin/Rejected")

        obj.order = None
