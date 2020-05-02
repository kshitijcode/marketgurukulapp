from django.db import models


# Create your models here.
class Quote(models.Model):
    symbol = models.CharField(max_length=20)
    current = models.DecimalField(decimal_places=2, max_digits=8)
    high = models.DecimalField(decimal_places=2, max_digits=8)
    low = models.DecimalField(decimal_places=2, max_digits=8)
    volume = models.IntegerField(default=0)
    average_volume = models.IntegerField(default=0.0)
    trend = models.CharField(max_length=10, default="NEUTRAL")
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.symbol)


class Stocks(Quote):
    recommendation = models.CharField(max_length=4, default="NEUTRAL")
