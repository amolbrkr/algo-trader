import argparse, sys
from utils import connect
from drivers import backtest
from utils import collect_data
from strategies import strategies


if __name__ == "__main__":
    arg_prsr = argparse.ArgumentParser()
    arg_prsr.add_argument("-gh", "--get_hist", help="Get historical stock data")
    arg_prsr.add_argument(
        "-t", "--run_test", help="Run a backtest using history data of a stock"
    )
    arg_prsr.add_argument("-s", "--start", help="Start date of test (YYYY-MM-DD)")
    arg_prsr.add_argument("-e", "--end", help="End date of test (YYYY-MM-DD)")
    arg_prsr.add_argument("-np", "--no_plot", help="No plotting")
    args = arg_prsr.parse_args()

    if args.get_hist:
        stocks = sys.argv[2].split(",")  # ["HDFC", "ITC", "TCS"]
        breeze = connect.ICICIConnector().connect()
        dc = collect_data.DataCollector(breeze)
        dc.get_stock_hist(stocks, "5minute", "2018-01-01", "2023-01-13")
        for s in stocks:
            dc.dump_to_csv(s)

    if args.run_test:
        feed = connect.Utils().read_data(sys.argv[2], args.start, args.end)
        bt = backtest.BTPYDriver(
            feed,
            strategies.TestStrat,
            cash=10000,
            commission=0.001,
            exclusive_orders=True,
        ).test
        print(bt.run())
        if not args.no_plot:
            bt.plot()
