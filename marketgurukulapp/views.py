import logging

from django.shortcuts import render
from django.views.generic.base import View

from .constants import TREND_DURATION
from .engine.recommend import Recommend
from .forms import UserInputForm
from .quote import QuoteService

logger = logging.getLogger(__name__)


def home(request):
    logger.info("Rendering the home page..")
    return render(request, 'marketgurukulapp/base.html')


class QuoteTodayView(View):

    def post(self, request):
        """
        :param request: Request PayLoad for Getting Quotes for a stock
        :return:
        """
        form = UserInputForm(request.POST)
        if form.is_valid():
            try:
                symbol = request.POST.get('symbol')
                # Initialising Quote Service
                qs = QuoteService(symbol)

                # Fetch Quotes
                stock = qs.get_quotes()

                # Fetch Trends
                days, prices = qs.get_trends(duration=TREND_DURATION)

                # Fetch Recommendation
                stock.recommendation = Recommend(stock).recommend()
                logger.debug(vars(stock))

                # Save to Database
                stock.save()
                logger.info("Saved to Database Successful")
                context = {'quote': stock, 'days': days, 'prices': prices, 'result': 'success'}
                return render(request, "marketgurukulapp/result.html", context=context)
            except (ValueError, Exception) as e:
                context = {'result': str(e)}
                logger.error(f"Value: {e}")
                return render(request, "marketgurukulapp/result.html", context=context)

        else:
            logger.error("Input Validation failed for SYMBOL")
            context = {'result': 'INPUT VALIDATERROR'}
            return render(request, "marketgurukulapp/result.html", context=context)
