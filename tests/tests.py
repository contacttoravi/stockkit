"""
@author: ravi
"""

import unittest
import datasource
import ticker
import os
from general import config
import matplotlib.pyplot as plt


class TestDataSource(unittest.TestCase):
    def setUp(self):
        pass

    def test_datasource_yahoo_1(self):
        ds = datasource.create('yahoo')
        self.assertEqual('yahoo', ds.name)

    def test_datasource_yahoo_2(self):
        ds = datasource.create('yahoo')
        mkt_data = ds.get_historic_prices('SBIN.NS', period='1mo')
        self.assertEqual('yahoo', ds.name)
        self.assertGreater(len(mkt_data), 10, "{} rows found in mkt_data".format(len(mkt_data)))

    def test_datasource_yahoo_3(self):
        # Test offline market-data functionality
        scrip = 'SBIN.NS'
        file_name = config['datasource']['file_location'] + "/{}/{}".format("yahoo", scrip)
        if os.path.isfile(file_name):
            os.remove(file_name)

        ds = datasource.create('yahoo')
        mkt_data = ds.get_historic_prices(scrip, period='1mo')
        self.assertEqual('yahoo', ds.name)
        self.assertGreater(len(mkt_data), 10, "{} rows found in mkt_data".format(len(mkt_data)))
        self.assertEqual(True, os.path.isfile(file_name))
        self.assertEqual(ds.source, "online")

        mkt_data = ds.get_historic_prices(scrip, period='1mo')
        self.assertEqual(ds.source, "offline")
        self.assertGreater(len(mkt_data), 10, "{} rows found in mkt_data".format(len(mkt_data)))

    def test_datasource_google_1(self):
        ds = datasource.create('google')
        self.assertEqual('google', ds.name)

    def test_ticker_purchased_1(self):
        # Short term strategy
        tk = ticker.TickerPurchased("SBIN.NS", "2020/06/01")
        tk.calculate_decisions('shortterm', target_csv_path='/stockkit/data/yahoo/SBIIN.NS.st.csv')

    def test_ticker_purchased_2(self):
        # Mid term strategy
        tk = ticker.TickerPurchased("SBIN.NS", "2020/06/01")
        tk.calculate_decisions('midterm', target_csv_path='/stockkit/data/yahoo/SBIIN.NS.mt.csv')

    def test_ticker_purchased_3(self):
        # Long term strategy
        tk = ticker.TickerPurchased("SBIN.NS", "2020/06/01")
        tk.calculate_decisions('longterm', target_csv_path='/stockkit/data/yahoo/SBIIN.NS.lt.csv')

    def test_macd(self):
        tk = ticker.TickerWatched("SBIN.NS")
        macd = tk.get_macd()
        macd.to_csv('/stockkit/data/yahoo/SBINS.macd.csv')
        macd.plot()
        plt.show()
