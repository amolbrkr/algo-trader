import talib as ta
from backtesting import Strategy
from backtesting.lib import crossover


class TestStrat(Strategy):
    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, 14)
        self.ema = self.I(ta.EMA, self.price, 6)
        self.ema1 = self.I(ta.EMA, self.price, 15)

    def next(self):
        ltp = self.data.Close[-1]
        tm = self.data.index[-1]

        if not self.position and tm.hour >= 15:
            return

        if not self.position:
            if (
                crossover(self.ema, self.ema1)
                and self.rsi[-1] >= 40
                and self.rsi[-1] <= 60
                and self.rsi[-3] < self.rsi[-2]
                and self.rsi[-2] < self.rsi[-1]
            ):
                sl = ltp - ltp * 0.004
                tp = ltp + ltp * 0.012

                self.buy(sl=sl, tp=tp)
        else:
            if tm.hour >= 15:
                self.trades[0].close()
                print(f"Mkt Close: {ltp}")
