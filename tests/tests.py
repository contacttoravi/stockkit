"""
@author: ravi
"""

import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/src/')

import datasource
import ticker
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


class TestPurchased(unittest.TestCase):
    def setUp(self):
        pass

    def test_ticker_purchased_1(self):
        # Short term strategy
        tk = ticker.TickerPurchased("SBIN.NS", "2021/05/01")
        tk.calculate_decisions('shortterm', target_csv_path='/stockkit/data/yahoo/SBIIN.NS.st.csv')

    def test_ticker_purchased_2(self):
        # Mid term strategy
        tk = ticker.TickerPurchased("SBIN.NS", "2021/05/01")
        tk.calculate_decisions('midterm', target_csv_path='/stockkit/data/yahoo/SBIIN.NS.mt.csv')

    def test_ticker_purchased_3(self):
        # Long term strategy
        tk = ticker.TickerPurchased("SBIN.NS", "2021/05/01")
        tk.calculate_decisions('longterm', target_csv_path='/stockkit/data/yahoo/SBIIN.NS.lt.csv')


class TestWatcher(unittest.TestCase):
    def setUp(self):
        pass

    def test_macd(self):
        tk = ticker.TickerWatched("SBIN.NS")
        macd = tk.get_macd()
        macd.to_csv('/stockkit/data/yahoo/SBINS.macd.csv')
        macd.plot()
        plt.show()

    def test_macd_pyplot(self):
        tk = ticker.TickerWatched("SBIN.NS")
        macd = tk.get_macd()
        macd.to_csv('/stockkit/data/yahoo/SBINS.macd.csv')

        fig, ax = plt.subplots(1)
        ax.plot(macd.Date, macd.macd, lw=2, label='macd', color='blue')
        ax.plot(macd.Date, macd.signal, lw=2, label='signal', color='red')
        fig.autofmt_xdate()
        ax.grid(True)
        ax.legend(loc='upper left')

        # Limit number of x labels to make it readable
        max_labels = 25
        xtickspace = int(len(macd.Date) / max_labels)
        if xtickspace > 0:
            for index, xlabel in zip(range(len(macd.Date)), ax.get_xticklabels()):
                if index % xtickspace == 0:
                    xlabel.set_visible(True)
                else:
                    xlabel.set_visible(False)
        plt.show()


test_cases = (TestDataSource, TestPurchased, TestWatcher)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True, verbosity=2)
    runner.run(load_tests(unittest.TestLoader(), None, None))
