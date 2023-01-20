import pandas as pd
import backtrader as bt


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

    def read_data(self, stock, start_dt, end_dt, filter_cols=True):
        res = pd.read_csv(
            f"hist_data/{stock}_data.csv",
            delimiter=",",
            index_col="datetime",
            parse_dates=True,
        )[f"{start_dt} 07:00:00":f"{end_dt} 16:00:00"]
        res = res[["open", "high", "low", "close", "volume"]] if filter_cols else res
        res.columns = map(str.title, res.columns)
        return res
