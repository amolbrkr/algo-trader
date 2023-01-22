import os
import json
import urllib
import webbrowser
import pandas as pd
from datetime import datetime
from breeze_connect import BreezeConnect


class ICICIConnector:
    def __init__(self):
        # Initialize SDK
        self.config = json.load(open("config.json"))
        self.breeze = BreezeConnect(api_key=self.config["api_key"])

    def __gen_session(self):
        self.breeze.generate_session(
            api_secret=self.config["api_secret"],
            session_token=self.session["api_session"],
        )
        return self.breeze

    def connect(self):
        today = datetime.now().strftime("%d-%m-%Y")
        self.session = (
            json.load(open(os.path.join(os.getcwd(), "session.json")))
            if os.path.exists("session.json")
            else None
        )
        if not self.session or self.session["generate_ts"] != today:
            webbrowser.open(
                "https://api.icicidirect.com/apiuser/login?api_key="
                + urllib.parse.quote_plus(self.config["api_key"]),
                new=0,
                autoraise=True,
            )
            self.session = {
                "api_session": input("Enter API Session: "),
                "generate_ts": today,
            }
            with open("session.json", "w") as sess_file:
                json.dump(self.session, sess_file)

        return self.__gen_session()

    def connect_ws(self):
        self.breeze.ws_connect()
        return self.breeze


class Utils:
    def read_data(self, stock, time_period, start_dt, end_dt, filter_cols=True):
        res = pd.read_csv(
            f"hist_data/{stock}_{time_period}_data.csv",
            delimiter=",",
            index_col="datetime",
            parse_dates=True,
        )[f"{start_dt} 07:00:00":f"{end_dt} 16:00:00"]
        res = res[["open", "high", "low", "close", "volume"]] if filter_cols else res
        res.columns = map(str.title, res.columns)
        print(
            f"Rows Loaded: {len(res.index)}, Min: {min(res.index)}, Max: {max(res.index)}"
        )
        return res
