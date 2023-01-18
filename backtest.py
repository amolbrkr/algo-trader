import time
import pytz
import pandas as pd
import backtrader as bt
from datetime import datetime, time
from strategies import EMAStrat


if __name__ == "__main__":
    stock = "ITC"

    cb = bt.Cerebro()
    cb.adddata(
        bt.feeds.PandasData(
            name=f"{stock} 5 Min",
            dataname=pd.read_csv(
                f"hist_data/{stock}_data.csv",
                delimiter=",",
                index_col="datetime",
                parse_dates=True,
            ),
            timeframe=bt.TimeFrame.Minutes,
            fromdate=datetime(2023, 1, 1),
            todate=datetime(2023, 1, 17),
            sessionstart=time(9, 5),
            sessionend=time(15, 25),
            tz=pytz.timezone("Asia/Kolkata"),
        )
    )
    cb.broker.set_cash(10000)
    cb.broker.set_coc(True)
    cb.addstrategy(EMAStrat)
    cb.addsizer(bt.sizers.PercentSizer, percents=90)
    print(f"Starting Portfolio Value: {cb.broker.getvalue()}")
    cb.run()
    print(f"Final Portfolio Value: {cb.broker.getvalue()}")
    cb.plot(style="candlestick")
