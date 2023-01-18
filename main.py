import connect
import collect_data


if __name__ == "__main__":
    breeze = connect.ICICIConnector().connect()
    dc = collect_data.DataCollector(breeze)
    stocks = ["HDFC", "ITC", "TCS"]
    dc.get_stock_hist(stocks, "5minute", "2018-01-01", "2023-01-13")
    for s in stocks:
        dc.dump_to_csv(s)
    
