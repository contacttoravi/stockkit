"""
@author: ravi
"""
from general import config
import datasource
from datetime import datetime
import pandas as pd

decisions = {'enter': "Initial entry",
             'hold': "Hold position",
             'sell': "Claim profit by selling a part of holdings",
             'exit': "Sell all holdings to stop further loss",
             'buy': "Buy more quantity as stock showing upward movement"}


class TickerPurchased(object):
    def __init__(self, ticker_name, start_date):
        """
        :param ticker_name: valid identifier for an instrument example "SBI", "INFOSYS"
        :param start_date: YYYY/MM/DD Initial date for analysis
        """
        self.ticker = ticker_name
        self.start_date = start_date
        self._validate_start_date()
        ds = datasource.create()
        self.prices = ds.get_historic_prices(self.ticker)
        self.decisions = pd.DataFrame()

    def _validate_start_date(self):
        date_today = datetime.today()
        date_start = datetime.strptime(self.start_date, "%Y/%m/%d")
        if date_start > date_today:
            raise Exception("start_date {} cannot be greater than today".format(self.start_date))
        date_diff = (date_today - date_start).days
        if date_diff >= 365:
            raise Exception("start_date is older than 365 days")

    @staticmethod
    def calculate_strategic_prices(price, strategy):
        sell_price = float(price) + (float(price) * int(config[strategy]["claim_profit_percent"])/100)
        exit_price = float(price) - (float(price) * int(config[strategy]["max_loss_percent"]) / 100)
        return sell_price, exit_price

    def calculate_decisions(self, strategy, addons=(), target_csv_path=None):
        """
        Analyse market price and assign a decision for that price
        Decisions: "SELL", "HOLD", "EXIT"
        :param strategy: name of decision strategy like shortterm, midterm, longterm
        :param target_csv_path: destination for report
        :param addons: List of additional decision points like watch_entire_market_movement,
        watch_financial_report, watch_news, etc
        :return: pandas.DataFrame time-series
        """
        print("Evaluating decisions")
        start_price = exit_price = sell_price = None
        curr_decision = None
        exit_found = False
        result_dates = []
        result_decisions = []
        result_prices = []

        for index, row in self.prices.iterrows():
            curr_date, curr_price = row['Date'], row['Close']
            if datetime.strptime(self.start_date, "%Y/%m/%d") >= datetime.strptime(curr_date, "%Y-%m-%d"):
                continue
            if not curr_price or curr_price == '':
                continue
            if not start_price:
                start_price = curr_price
                sell_price, exit_price = self.calculate_strategic_prices(curr_price, strategy)
                print("enter(date, price) = ({},{})".format(curr_date, curr_price))
                curr_decision = "enter"
            elif exit_found:
                curr_decision = "exit"
            elif float(curr_price) < exit_price:
                curr_decision = "exit"
                exit_found = True
                print("exit(date, price) = ({},{})".format(curr_date, curr_price))
            elif float(curr_price) > sell_price:
                curr_decision = "sell"
                print("sell(date, price) = ({},{})".format(curr_date, curr_price))
                sell_price, exit_price = self.calculate_strategic_prices(curr_price, strategy)
            else:
                curr_decision = "hold"

            result_dates.append(curr_date)
            result_prices.append("{:.2f}".format(curr_price))
            result_decisions.append(curr_decision)

        self.decisions = pd.DataFrame({'Date': result_dates,
                                       'Close': result_prices,
                                       'Decision': result_decisions})

        if target_csv_path:
            self.decisions.to_csv(target_csv_path)
        print("Completed evaluating decisions")
        return self.decisions


class TickerWatched(object):
    def __init__(self, ticker_name, start_date=None):
        """
        :param ticker_name: valid identifier for an instrument example "SBI", "INFOSYS"
        """
        self.ticker = ticker_name
        ds = datasource.create()
        self.prices = ds.get_historic_prices(self.ticker)
        if len(self.prices) < 10:
            raise Exception("Insufficient data to watch ticker {}".format(ticker_name))
        self.decisions = pd.DataFrame()

    @staticmethod
    def calculate_strategic_prices(price, strategy):
        """
        sell_price = float(price) + (float(price) * int(config[strategy]["claim_profit_percent"])/100)
        exit_price = float(price) - (float(price) * int(config[strategy]["max_loss_percent"]) / 100)
        return sell_price, exit_price
        """
        # TODO: TBD
        pass

    def calculate_decisions(self, strategy, addons=(), target_csv_path=None):
        """
        Analyse market price and assign "BUY" decision for that price
        :param strategy: name of decision strategy like shortterm, midterm, longterm
        :param target_csv_path: destination for report
        :param addons: List of additional decision points like watch_entire_market_movement,
        watch_financial_report, watch_news, etc
        :return: pandas.DataFrame time-series
        """
        print("Evaluating decisions")
        buy_price = None
        curr_decision = None
        result_dates = []
        result_decisions = []
        result_prices = []

        for index, row in self.prices.iterrows():
            # TODO: TBD
            curr_date, curr_price = row['Date'], row['Close']

            result_dates.append(curr_date)
            result_prices.append("{:.2f}".format(curr_price))
            result_decisions.append(curr_decision)

        self.decisions = pd.DataFrame({'Date': result_dates,
                                       'Close': result_prices,
                                       'Decision': result_decisions})

        if target_csv_path:
            self.decisions.to_csv(target_csv_path)
        print("Completed evaluating decisions")
        return self.decisions

    def get_macd(self, fast=12, slow=26, signal=9):
        """
        Calculate Moving Average
        :param fast:
        :param slow:
        :param signal:
        :return:
        """
        cl_prices = self.prices[['Date', 'Close']].copy()
        cl_prices['ma_fast'] = cl_prices['Close'].ewm(span=fast, min_periods=fast).mean()
        cl_prices['ma_slow'] = cl_prices['Close'].ewm(span=slow, min_periods=slow).mean()
        cl_prices['macd'] = cl_prices['ma_fast'] - cl_prices['ma_slow']
        cl_prices['signal'] = cl_prices['macd'].ewm(span=signal, min_periods=signal).mean()
        cl_prices.dropna(inplace=True)
        return cl_prices[['Date', 'macd', 'signal']].copy()
