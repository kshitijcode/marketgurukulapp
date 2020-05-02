import logging

import numpy as np

from ..alphavantage import AlphaVantageService
from ..constants import RECOMMENDATION,LOOKBACK_FOR_CROSSOVER

logger = logging.getLogger(__name__)


class Recommend(object):

    def __init__(self, quote):
        self.quote = quote
        self.signals = {}
        self.duration = 100
        self.slow_window = 200
        self.fast_window = 50
        self.ema_signal = RECOMMENDATION.NOACTION

    def recommend(self):
        """
        This method returns buy and sell signals based on EMA Cross Over Strategy.
        :return:
        """
        logger.info(f"Fetching Recommendations for stock {self.quote.symbol}")
        # Fetch slower and faster EMA From AlphaVantageAPI
        shorter_sma = AlphaVantageService(self.quote.symbol).get_ema(window=self.fast_window, symbol=self.quote.symbol,
                                                                     duration=self.duration,
                                                                     interval='daily')
        longer_sma = AlphaVantageService(self.quote.symbol).get_ema(window=self.slow_window, symbol=self.quote.symbol,
                                                                    duration=self.duration,
                                                                    interval='daily')
        logger.debug("Shorter SMA " + str(shorter_sma))
        logger.debug("Longer SMA" + str(longer_sma))
        # Check if shorter SMA is greater than longer SMA
        self.signals['signal'] = np.where(
            shorter_sma[self.fast_window:] > longer_sma[self.fast_window:], 1.0, 0.0)

        # Checks for cross over by looking for a difference between subsequent time series values for positions
        self.signals['positions'] = np.diff(self.signals['signal'], axis=0)

        # Check average Average Volume for Recommendation
        volume_confirmation = True if self.quote.volume >= self.quote.average_volume else False

        # Check for cross over in last 30 days
        for value in self.signals['positions'][LOOKBACK_FOR_CROSSOVER:]:
            if value >= 1 and volume_confirmation:
                self.ema_signal = RECOMMENDATION.BUY
                break
            elif value < 0:
                self.ema_signal = RECOMMENDATION.SELL
                break

        return self.ema_signal
