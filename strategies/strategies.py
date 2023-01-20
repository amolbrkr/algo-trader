from backtesting.test import SMA
from backtesting.lib import crossover
from backtesting import Strategy


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
        # print(f"{order_type}: {price}, SL: {sl}, TP: {tp}")
        return (price, sl, tp)


class TestStrat(BaseStrat):
    def init(self):
        self.sma1 = self.I(SMA, self.price, 10)
        self.sma2 = self.I(SMA, self.price, 50)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.execute("BUY", self.data.Close[-1])
        elif crossover(self.sma2, self.sma1):
            self.execute("SELL", self.data.Close[-1])