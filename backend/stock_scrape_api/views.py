from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.templatetags.static import static
from .serializers import StockSerializer
from .stock_scraper import get_current_price, get_prev_week_endpoints, market_open
from .models import Stock
from datetime import datetime
from pytz import timezone, utc as utc_timezone

import json
import os
import sys

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'static/stock_scrape_api/tickers.json')
with open(filename, 'rb') as f:
    tickers = json.load(f)

# create some views

def home_view(request):
    return render(request, 'home.html', {})

@api_view(['GET'])
def current_price(request, ticker):
    ticker = ticker.upper()
    try:
        stock = Stock.objects.get(ticker=ticker)
    except Stock.DoesNotExist:
        if ticker in tickers:
            stock = Stock(ticker=ticker.upper(), name=tickers[ticker])
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    stock.update()
    # stock.save()
    serializer = StockSerializer(stock, many=False)
    sys.stdout.flush()
    return Response(serializer.data)

    
