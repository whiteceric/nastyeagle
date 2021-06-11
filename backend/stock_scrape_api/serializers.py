from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['ticker', 'name', 'latest_price', 'latest_day_change', 'last_updated']
