import itertools

import numpy as np
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from yahoo_fin import stock_info as si


class AlphaVantageService:
    def __init__(self, symbol):
        self.key = 'AN4QDZQ58QJ32E0K'
        self.symbol = symbol
        self.technical_indicator = TechIndicators(self.key)
        self.time_series = TimeSeries(self.key)
        self.data, _ = self.time_series.get_daily(symbol=symbol)

    def get_ema(self, window, symbol, interval, duration):
        symbol_ema, _ = self.technical_indicator.get_ema(symbol=symbol, time_period=window, interval=interval)
        sliced_ema = dict(itertools.islice(symbol_ema.items(), duration))
        ema_values_list = []
        for ema_value in sliced_ema:
            ema_values_list.append(float(sliced_ema[ema_value]['EMA']))
        return np.array(ema_values_list)

    def get_daily_trends(self, duration):
        sliced_days = dict(itertools.islice(self.data.items(), duration))
        prices = []
        for price in sliced_days:
            prices.append(float(sliced_days[price]['4. close']))
        return list(sliced_days.keys())[::-1], prices[::-1]

    def get_current(self):
        return round(si.get_live_price(self.symbol), 2)

    def get_high(self):
        return self.get_last_day_data()['2. high']

    def get_low(self):
        return self.get_last_day_data()['3. low']

    def get_trend(self):
        if float(self.get_current()) >= float(self.get_last_day_data()['4. close']):
            return "POSITIVE"
        else:
            return "NEGATIVE"

    def get_volume(self):
        return int(self.get_last_day_data()['5. volume'])

    def get_average_volume(self):
        dates = list(self.data.keys())[0:10]
        volumes = []
        for date in dates:
            volumes.append(int(self.data[date]['5. volume']))
        return float(np.average(volumes))

    def get_day_data(self, day):
        return self.data[day]

    def get_last_day_data(self):
        return self.data[list(self.data.keys())[0]]
