import math
import talib as ta
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover


class TestStrat(Strategy):
    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, 14)
        self.atr = self.I(
            ta.ATR, self.data.High, self.data.Low, self.price, 14, plot=False
        )
        self.ema = self.I(ta.EMA, self.price, 18)
        self.ema1 = self.I(ta.EMA, self.price, 36)

    def next(self):
        tm = self.data.index[-1]
        ltp = self.data.Close[-1]
        ltp_open = self.data.Open[-1]
        slope0 = math.degrees(math.atan(self.ema[-1] - self.ema[-2]))
        slope = math.degrees(math.atan(self.ema1[-1] - self.ema1[-2]))
        print(
            f"{tm}: {slope}, {slope0 - slope}, {crossover(self.ema, self.ema1)}, {self.atr[-1]}"
        )

        if not self.position and tm.hour >= 15:
            return

        if not self.position:
            if (
                ltp_open < self.ema
                and ltp > self.ema
                and ltp_open < self.ema1
                and ltp > self.ema1
                and self.atr[-1] >= 3.5
                and slope >= 3
                and self.rsi[-1] >= 40
                and self.rsi[-1] <= 80
            ):
                # sl = ltp - ltp * 0.005
                sl = ltp - self.atr[-1] * 1.5
                tp = ltp + ltp * 0.015
                self.buy(sl=sl, tp=tp)
                print(f"BUY: {ltp}, SL: {sl}, TP: {tp}")
            elif (
                ltp_open > self.ema
                and ltp < self.ema
                and ltp_open > self.ema1
                and ltp < self.ema1
                and self.atr[-1] >= 3.5
                and slope < 0
                and self.rsi[-1] >= 40
                and self.rsi[-1] <= 80
                # and crossover(self.ema1, self.ema)
            ):
                sl = ltp + self.atr[-1] * 1.5
                tp = ltp - ltp * 0.015
                self.sell(sl=sl, tp=tp)
                print(f"SELL: {ltp}, SL: {sl}, TP: {tp}")
        else:
            # if tm.hour >= 15:
            #     self.position.close()
            #     print(f"Mkt Close: {ltp}")

            if self.position.is_long and crossover(self.ema, self.price):
                self.position.close()
                print(f"Buy Close: {ltp}")
            elif self.position.is_short and crossover(self.price, self.ema):
                self.position.close()
                print(f"Sell Close: {ltp}")
