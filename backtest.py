import time
import pytz
import pandas as pd
import backtrader as bt
from datetime import datetime, time
from strategies import EMAStrat


if __name__ == "__main__":
    stock = "TCS"

    cb = bt.Cerebro()
    cb.adddata(
        # cb.resampledata(
            bt.feeds.PandasData(
                name=f"{stock} 5 Min",
                dataname=pd.read_csv(
                    f"hist_data/{stock}_data.csv",
                    delimiter=",",
                    index_col="datetime",
                    parse_dates=True,
                )["2022-01-01 07:00:00": "2023-01-18 16:00:00"],
                timeframe=bt.TimeFrame.Minutes,
                fromdate=datetime(2022, 1, 1),
                todate=datetime(2023, 1, 18),
                sessionstart=time(9, 5),
                sessionend=time(15, 25),
                tz=pytz.timezone("Asia/Kolkata"),
            ),
        #     timeframe=bt.TimeFrame.Minutes,
        #     rightedge=False,
        #     compression=1,
        # )
    )
    cb.broker.set_cash(10000)
    cb.addstrategy(EMAStrat)
    cb.addsizer(bt.sizers.PercentSizer, percents=100)
    print(f"Starting Portfolio Value: {cb.broker.getvalue()}")
    cb.run()
    print(f"Final Portfolio Value: {cb.broker.getvalue()}")
    cb.plot(style="candlestick")
