from .alphavantage import AlphaVantageService
from .models import Stocks
from .constants import VOLUME_PERIOD

import logging

logger = logging.getLogger(__name__)


class QuoteService(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self.avs = AlphaVantageService(symbol=symbol)

    def get_quotes(self):
        """
        VOLUME_PERIOD: Number of Days the Volume needs to averaged out to.
        :return: Returns the Stocks Model Object with the populated fields
        """
        logger.info("Fetching Quotes")
        high = self.avs.get_high()
        low = self.avs.get_low()
        current = self.avs.get_current()
        trend = self.avs.get_trend()
        volume = self.avs.get_volume()
        average_volume = self.avs.get_average_volume(VOLUME_PERIOD)
        quote = Stocks(symbol=self.symbol, current=current, high=high, low=low, trend=trend, volume=volume,
                       average_volume=average_volume)
        return quote

    def get_trends(self, duration):
        """
        Returns the Trends based upon duration
        :param duration: number of days for which the trend is needed
        :return: daily and prices lists
        """
        logger.info("Fetching Trends")
        return self.avs.get_daily_trends(duration=duration)
