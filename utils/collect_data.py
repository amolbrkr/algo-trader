import time
import pandas as pd
from datetime import datetime


class DataCollector:
    def __init__(self, breeze):
        self.store = dict()
        self.breeze = breeze

    def get_stock_hist(self, stock_list, interval, start_dt, end_dt):
        stock_code = self.breeze.get_names(exchange_code="NSE", stock_code="TATASTEEL")
        print(stock_code)
        res = self.breeze.get_historical_data(
            interval="30minute",
            from_date=f"2015-01-01T09:00:00.000Z",
            to_date=f"2023-01-24T15:30:00.000Z",
            stock_code=stock_code["isec_stock_code"],
            exchange_code="NSE",
            product_type="cash",
        )
        print(res["Status"], res["Error"], res.get("Success"))
        print(len(res["Success"].index))
        exit()

        res = list()
        start = datetime.strptime(start_dt, "%Y-%m-%d")
        end = datetime.strptime(end_dt, "%Y-%m-%d")

        for stock in stock_list:
            try:
                print(stock)
                res = self.breeze.get_historical_data_v2(
                    interval=interval,
                    from_date=f"{start_dt}T09:00:00.000Z",
                    to_date=f"{end_dt}T16:00:00.000Z",
                    stock_code=stock,
                    exchange_code="NSE",
                    product_type="cash",
                )

                print(f"Status: {res['Status']}, Error: {res['Error']}")
                if "Success" in res.keys():
                    self.store[stock] = {
                        "data": pd.DataFrame(res["Success"]),
                        "interval": interval,
                    }
                    print(f"Len: {len(self.store[stock]['data'].index)}")
                    print(f"Min: {min(self.store[stock]['data']['datetime'])}")
                    print(f"Max: {max(self.store[stock]['data']['datetime'])}")
                    print(f"---------")
            except Exception as e:
                print(f"Fetch Error: {e}")
                continue

    def dump_to_csv(self, stock):
        if stock not in self.store.keys():
            print("Error: Stock code not in store.")
        else:
            self.store[stock]["data"].to_csv(
                f"hist_data/{stock}_{self.store[stock]['interval']}_data.csv"
            )
