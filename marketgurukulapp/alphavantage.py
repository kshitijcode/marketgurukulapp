import itertools
import logging
import os

import numpy as np
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from yahoo_fin import stock_info as si

from .constants import TREND

logger = logging.getLogger(__name__)


class AlphaVantageService:
    def __init__(self, symbol):
        self.key = os.getenv('ALPHAVANTAGE_SECRET_KEY')
        self.symbol = symbol
        self.technical_indicator = TechIndicators(self.key)
        self.time_series = TimeSeries(self.key)
        self.data, _ = self.time_series.get_daily(symbol=symbol)

    def get_ema(self, window, symbol, interval, duration):
        """

        :param window: Slinding window for Moving Average operations
        :param symbol: Symbol of Stock
        :param interval: Interval for consecutive data points eg. daily,weekly,monthly
        :param duration: how far behind the data needs to be evaluated for( value is in days)
        :return: return the moving average series for each data point
        """
        try:
            symbol_ema, _ = self.technical_indicator.get_ema(symbol=symbol, time_period=window, interval=interval)
            sliced_ema = dict(itertools.islice(symbol_ema.items(), duration))
            ema_values_list = []
            for ema_value in sliced_ema:
                ema_values_list.append(float(sliced_ema[ema_value]['EMA']))
            logger.debug(ema_values_list)
            return np.array(ema_values_list)
        except Exception as e:
            logger.error("ERROREMA : ERROR FETCHING EMA")
            raise Exception("ERROREMA")

    def get_daily_trends(self, duration):
        """
        Returns price and daily trend for a duration
        :param duration: the number of days for which the data needs to be sent.
        :return:
        """
        try:
            sliced_days = dict(itertools.islice(self.data.items(), duration))
            prices = []
            for price in sliced_days:
                prices.append(float(sliced_days[price]['4. close']))
            logger.debug(str(sliced_days))
            return list(sliced_days.keys())[::-1], prices[::-1]
        except Exception as e:
            logger.error("ERRORDAILYTRENDS : Error Parsing Daily Trends")
            raise Exception("ERRORDAILYTRENDS")

    def get_current(self):
        """

        :return:
        """
        return round(si.get_live_price(self.symbol), 2)

    def get_high(self):
        """

        :return:
        """
        return self.get_last_day_data()['2. high']

    def get_low(self):
        """

        :return:
        """
        return self.get_last_day_data()['3. low']

    def get_trend(self):
        """

        :return:
        """
        if float(self.get_current()) >= float(self.get_last_day_data()['4. close']):
            return TREND.POSITIVE
        else:
            return TREND.NEGATIVE

    def get_volume(self):
        """

        :return:
        """
        return int(self.get_last_day_data()['5. volume'])

    def get_average_volume(self, volume_period):
        """
\
        :param volume_period:
        :return:
        """
        dates = list(self.data.keys())[0:volume_period]
        volumes = []
        for date in dates:
            volumes.append(int(self.data[date]['5. volume']))
        return float(np.average(volumes))

    def get_day_data(self, day):
        """

        :param day:
        :return:
        """
        return self.data[day]

    def get_last_day_data(self):
        """

        :return:
        """
        return self.data[list(self.data.keys())[0]]
