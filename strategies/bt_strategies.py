import backtrader as bt


class BaseStrat(bt.Strategy):
    def execute(self, order_type, price, sl_pcnt=0.004, tp_pcnt=0.012):
        sl, tp = (
            price - price * sl_pcnt if order_type == "BUY" else price + price * sl_pcnt,
            price + price * tp_pcnt if order_type == "BUY" else price - price * tp_pcnt,
        )
        if order_type == "BUY":
            self.buy()
        else:
            self.sell()
        print(f"{order_type}: {price}, SL: {sl}, TP: {tp}")
        return (price, sl, tp)


class EMAStrat(BaseStrat):
    def __init__(self):
        self.scnt = self.fcnt = 0
        self.price = self.data0.close
        self.rsi = bt.ind.RSI(plot=False)
        self.ema = bt.ind.ZeroLagExponentialMovingAverage(period=200)
        self.cross = bt.ind.CrossOver(self.price, self.ema, plot=False)

    def next(self):
        print(f"{self.datetime.datetime(0)} - {self.price[0]}")
        if not self.position and self.datetime.datetime(0).hour >= 15:
            return

        if not self.position:
            if (
                (self.cross[0] > 0 or self.cross[-1] > 0)
                and self.rsi >= 40
                and self.rsi <= 60
                and self.rsi[0] > self.rsi[-1]
                and self.rsi[-1] > self.rsi[-2]
            ):
                self.bp, self.sl, self.tp = self.execute("BUY", self.price[0])
        else:
            if self.datetime.datetime(0).hour >= 15:
                chg = self.price[0] - self.bp
                if chg > 0:
                    self.scnt += 1
                else:
                    self.fcnt += 1
                print(f"Mkt Close: {chg}")
                self.sell()
            elif self.price <= self.sl:
                print(f"Stop Loss: {self.bp - self.price[0]}")
                self.fcnt += 1
                self.sell()
            elif self.price >= self.tp:
                print(f"Take Profit: {self.price[0] - self.bp}")
                self.scnt += 1
                self.sell()

    def stop(self):
        print(
            f"T: {self.scnt + self.fcnt} S: {self.scnt}, F: {self.fcnt}, Win%: {self.scnt / (self.scnt + self.fcnt) * 100}"
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
