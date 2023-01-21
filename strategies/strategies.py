import talib as ta
from backtesting import Strategy
from backtesting.lib import crossover


class BaseStrat(Strategy):
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
                self.buy(sl=ltp - ltp * 0.004, tp=ltp + ltp * 0.012)
        else:
            if tm.hour >= 15:
                self.trades[0].close()
                print(f"Mkt Close: {ltp}")
