import math
import talib as ta
import pandas as pd
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
        slope = math.degrees(math.atan(self.ema1[-1] - self.ema1[-2]))

        if not self.position and tm.hour >= 15:
            return

        if not self.position:
            if (
                (crossover(self.price, self.ema) or crossover(self.ema, self.ema1))
                and self.rsi[-1] >= 40
                and self.rsi[-1] <= 80
                and slope >= 3
            ):
                sl = ltp - ltp * 0.005
                tp = ltp + ltp * 0.015

                self.buy(sl=sl, tp=tp)
                print(f"BUY: {ltp}, SL: {sl}, TP: {tp}")
        else:
            if tm.hour >= 15 or crossover(self.ema1, self.ema):
                self.position.close()
                print(f"Mkt Close: {ltp}")
