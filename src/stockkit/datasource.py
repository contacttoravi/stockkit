"""
@author: ravi
"""

import yfinance
from pandas import DataFrame, read_csv
from stockkit.general import config, Methods
from os import path, mkdir


class DataSource(object):
    def __init__(self, name):
        self.name = name

    def get_historic_prices(self, ticker, period):
        pass

    def _write_to_file(self):
        pass

    def _read_from_file(self):
        pass


class GoogleFinance(DataSource):
    def __init__(self):
        super().__init__("google")

    def get_historic_prices(self, ticker, period):
        pass


class YahooFinance(DataSource):
    def __init__(self):
        super().__init__("yahoo")
        self.downloaded_data = DataFrame()
        self.ticker = None
        self.source = None

    def get_historic_prices(self, ticker, period='1y', try_offline=True):
        self.ticker = ticker
        if try_offline and self._read_from_file():
            self.source = "offline"
            return self.downloaded_data

        print("Fetching online for ticker {}".format(ticker))
        self.downloaded_data = yfinance.download(self.ticker, period=period)
        self._validate_downloaded_data()
        self.source = "online"
        self.downloaded_data.fillna(method='ffill', inplace=True)
        self._write_to_file()
        self._read_from_file()  # Need to explicitly read file to add 'Date' is a column in DataFrame
        return self.downloaded_data

    def _validate_downloaded_data(self):
        if len(self.downloaded_data) < 10:
            raise Exception("Insufficient market data for ticker {}".format(self.ticker))
        if float(self.downloaded_data.mean()['Close']) <= 0.0:
            raise Exception("Market data showing 0 for ticker {}".format(self.ticker))
        return True

    def _write_to_file(self):
        base_path = config['datasource']['file_location'] + "/{}".format("yahoo")
        file_name = base_path + "/{}".format(self.ticker)
        if not path.isdir(base_path):
            mkdir(base_path)
        self.downloaded_data.to_csv(file_name)

    def _read_from_file(self):
        file_name = config['datasource']['file_location'] + "/{}/{}".format("yahoo", self.ticker)
        if path.isfile(file_name) and not Methods.is_file_older_than_x_days(file_name, 1):
            self.downloaded_data = read_csv(file_name)
            return True
        else:
            return False


def create(name=None):
    """
    Returns DataSource implementation object
    :param name: If not provided, a default name from config is picked up
    :return: DataSource implementation object
    """
    AVAILABLE_DATASOURCE = {'yahoo': YahooFinance, 'google': GoogleFinance}
    try:
        if not name:
            name = config['datasource']['name']
        return AVAILABLE_DATASOURCE[name]()
    except:
        raise Exception("Available sources are: {}".format(AVAILABLE_DATASOURCE.keys()))
