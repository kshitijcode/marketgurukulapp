from unittest.mock import patch, Mock

from django.test import TestCase

import marketgurukulapp
from .alphavantage import AlphaVantageService


# Create your tests here.

class AlphaVantageAPIServiceTestCase(TestCase):
    def setUp(self):
        self.symbol = "AAPL"
        self.avs = AlphaVantageService(self.symbol)

    def test_AAPL_daily_quote(self):
        data = self.avs.get_day_data('2020-04-30')
        self.assertEqual(float(data['4. close']), 293.8000)

    @patch('marketgurukulapp.alphavantage.AlphaVantageService.get_low')
    def test_AAPL_daily_quote(self, mock_avs):
        mock_avs.return_value = "123.00"
        result = mock_avs()
        self.assertEqual(mock_avs.call_count,1)


class QuoteSaveTest(TestCase):
    def setUp(self):
        self.symbol = "AAPL"
        self.current = 1.0
        self.high = 1.0
        self.low = 1.0
        self.volume = 0
        self.average_volume = 0

    @patch('marketgurukulapp.models.Stocks')
    def test_save_to_db(self, stock_mock):
        save_mock = Mock(return_value=None)
        stock_mock.save = save_mock
        quote = marketgurukulapp.models.Stocks(symbol=self.symbol, current=self.current, high=self.high, low=self.low,
                                               volume=self.volume,
                                               average_volume=self.average_volume)
        quote.save()
        self.assertEqual(stock_mock.call_count, 1)
        self.assertEqual(save_mock.call_count, 0)
