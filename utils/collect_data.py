import time
import pandas as pd
from datetime import datetime


class DataCollector:
    def __init__(self, breeze):
        self.store = dict()
        self.breeze = breeze

    def get_stock_hist(self, stock_list, interval, start_dt, end_dt):
        res = list()
        start = datetime.strptime(start_dt, "%Y-%m-%d")
        end = datetime.strptime(end_dt, "%Y-%m-%d")

        for stock in stock_list:
            print(stock)
            res = self.breeze.get_historical_data(
                interval=interval,
                from_date=f"{start_dt}T07:00:00.000Z",
                to_date=f"{end_dt}T07:00:00.000Z",
                stock_code=stock,
                exchange_code="NSE",
                product_type="cash",
            )

            if "Success" in res.keys():
                print(res)
                self.store[stock] = {
                    "data": pd.DataFrame(res["Success"]),
                    "interval": interval,
                }
                print(f"Len: {len(self.store[stock].index)}")
                print(f"Min: {min(self.store[stock]['datetime'])}")
                print(f"Max: {max(self.store[stock]['datetime'])}")

    def dump_to_csv(self, stock):
        if stock not in self.store.keys():
            print("Error: Stock code not in store.")
        else:
            self.store[stock]["data"].to_csv(
                f"hist_data/{stock}_{self.store[stock]['interval']}_data.csv"
            )
