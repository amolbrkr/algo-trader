import backtrader as bt

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
