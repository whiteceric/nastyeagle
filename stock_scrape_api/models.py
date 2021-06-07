from django.db import models

class Symbol(models.Model):
    ticker = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255, blank=True)
    latest_price = models.FloatField(blank=True)
    latest_day_change = models.FloatField(blank=True)
    last_updated = models.DateTimeField(blank=True)

    def __str__(self):
        return self.tag
