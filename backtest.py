import time
import pytz
import pandas as pd
import backtrader as bt
from datetime import datetime, time
from strategies import EMAStrat


if __name__ == "__main__":
    stock = "TCS"
    df = pd.read_csv(
        f"hist_data/{stock}_data.csv",
        delimiter=",",
        index_col="datetime",
        parse_dates=True,
    )
    data = bt.feeds.PandasData(
        name=f"{stock} 5 Min",
        dataname=df,
        timeframe=bt.TimeFrame.Minutes,
        fromdate=datetime(2023, 1, 1),
        todate=datetime(2023, 1, 17),
        sessionstart=time(9, 5),
        sessionend=time(15, 25),
        tz=pytz.timezone("Asia/Kolkata"),
    )

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.broker.set_coc(True)
    cerebro.addstrategy(EMAStrat)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.plot(style="candlestick")
