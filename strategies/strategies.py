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


class TestStrat(BaseStrat):
    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, 14)
        self.ema = self.I(ta.EMA, self.price, 5)
        self.ema1 = self.I(ta.EMA, self.price, 15)

    def next(self):
        in_mkt = False
        ltp = self.data.Close[-1]

        if (
            crossover(self.ema, self.ema1)
            and self.rsi[-1] >= 40
            and self.rsi[-1] <= 60
            and self.rsi[-3] < self.rsi[-2]
            and self.rsi[-2] < self.rsi[-1]
        ):
            self.bp, self.sl, self.tp = self.execute("BUY", ltp)
            in_mkt = True

        if in_mkt and (
            self.data.index[-1].hour >= 15 or ltp <= self.sl or ltp >= self.tp
        ):
            self.sell()
