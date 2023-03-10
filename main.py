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
    arg_prsr.add_argument("-tp", "--time_period", help="Time period of data to fetch")
    args = arg_prsr.parse_args()

    if args.get_hist:
        stocks = sys.argv[2].split(",")
        breeze = connect.ICICIConnector().connect()
        dc = collect_data.DataCollector(breeze)
        dc.get_stock_hist(stocks, args.time_period, args.start, args.end)
        for s in stocks:
            dc.dump_to_csv(s)

    if args.run_test:
        feed = connect.Utils().read_data(
            sys.argv[2], args.time_period, args.start, args.end
        )
        bt = backtest.BTPYDriver(
            feed,
            strategies.TestStrat,
            cash=10000,
            commission=0.001,
            exclusive_orders=True,
        ).test
        print(bt.run())
        # df = pd.DataFrame(out._strategy.slope_vals)
        # print(f"Min: {min(df['slope'])}, Max: {max(df['slope'])}")
        if not args.no_plot:
            try:
                bt.plot(open_browser=False)
            except Exception as e:
                print(f"Plot Error: {e}")
