from django.shortcuts import render
from django.views.generic.base import View

from .engine.recommend import Recommend
from .quote import QuoteService

import logging

logger = logging.getLogger(__name__)


def home(request):
    logger.debug("Rendering the home page..")
    return render(request, 'marketgurukulapp/base.html')


class QuoteTodayView(View):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        symbol = request.GET.get('search')
        qs = QuoteService(symbol)
        stock = qs.get_quotes()
        stock.recommendation = Recommend(stock).recommend()
        days, prices = qs.get_trends(duration=30)
        stock.save()
        context = {'quote': stock, 'days': days, 'prices': prices}
        return render(request, "marketgurukulapp/result.html", context=context)
