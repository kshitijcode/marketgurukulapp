import numpy as np

from ..alphavantage import AlphaVantageService


class Recommend(object):
    def __init__(self, quote):
        self.quote = quote
        self.signals = {}
        self.duration = 100
        self.slow_window = 200
        self.fast_window = 50
        self.ema_signal = "NOACTION"

    def recommend(self):
        shorter_sma = AlphaVantageService(self.quote.symbol).get_ema(window=self.fast_window, symbol=self.quote.symbol,
                                                                     duration=self.duration,
                                                                     interval='daily')
        longer_sma = AlphaVantageService(self.quote.symbol).get_ema(window=self.slow_window, symbol=self.quote.symbol,
                                                                    duration=self.duration,
                                                                    interval='daily')

        self.signals['signal'] = np.where(
            shorter_sma[self.fast_window:] > longer_sma[self.fast_window:], 1.0, 0.0)
        self.signals['positions'] = np.diff(self.signals['signal'], axis=0)

        for value in self.signals['positions'][-30:]:
            if value >= 1:
                self.ema_signal = "BUY"
                break
            elif value < 0:
                self.ema_signal = "SELL"
                break

        volume_confirmation = True if self.quote.volume >= self.quote.average_volume else False

        if volume_confirmation:
            return self.ema_signal
        else:
            return "SELL"
