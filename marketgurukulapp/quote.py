from .alphavantage import AlphaVantageService
from .models import Stocks


class QuoteService(object):

    def __init__(self, symbol):
        self.symbol=symbol
        self.avs = AlphaVantageService(symbol=symbol)

    def get_quotes(self):
        high = self.avs.get_high()
        low = self.avs.get_low()
        current = self.avs.get_current()
        trend = self.avs.get_trend()
        volume = self.avs.get_volume()
        average_volume = self.avs.get_average_volume()
        quote = Stocks(symbol=self.symbol, current=current, high=high, low=low, trend=trend, volume=volume,
                       average_volume=average_volume)
        return quote

    def get_trends(self,duration):
        return self.avs.get_daily_trends(duration=duration)
