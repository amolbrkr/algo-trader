import time
import pandas as pd
from datetime import datetime, timedelta


class DataCollector:
    def __init__(self, breeze):
        self.store = dict()
        self.breeze = breeze

    def get_stock_hist(self, stock_list, interval, start_dt, end_dt):
        fmt = "%Y-%m-%d"
        num_days = timedelta(days=1000 // (375 // int(interval[:2])))
        start = datetime.strptime(start_dt, fmt)
        end = datetime.strptime(end_dt, fmt)

        for stock in stock_list:
            print(stock)
            stock_data = res = list()
            stk_nm = self.breeze.get_names(exchange_code="NSE", stock_code=stock)
            try:
                cut_off = start + num_days
                while cut_off < end:
                    print(f"Fetching {start} - {cut_off}")
                    res = self.breeze.get_historical_data_v2(
                        interval=interval,
                        from_date=f"{start.strftime(fmt)}T09:00:00.000Z",
                        to_date=f"{cut_off.strftime(fmt)}T16:00:00.000Z",
                        stock_code=stk_nm["isec_stock_code"],
                        exchange_code="NSE",
                        product_type="cash",
                    )

                    print(f"Status: {res['Status']}, Error: {res['Error']}")
                    if "Success" in res.keys():
                        stock_data.extend(res["Success"])
                        print(f"Done, total records: {len(stock_data)}.")
                    start = cut_off
                    cut_off += num_days
            except Exception as e:
                print(f"Fetch Error: {e}")
                continue
            self.store[stock] = {
                "data": pd.DataFrame(res["Success"]),
                "interval": interval,
            }
            print(f"Len: {len(self.store[stock]['data'].index)}")
            print(f"Min: {min(self.store[stock]['data']['datetime'])}")
            print(f"Max: {max(self.store[stock]['data']['datetime'])}")
            print(f"---------")

    def dump_to_csv(self, stock):
        if stock not in self.store.keys():
            print("Error: Stock code not in store.")
        else:
            self.store[stock]["data"].to_csv(
                f"hist_data/{stock}_{self.store[stock]['interval']}_data.csv"
            )
