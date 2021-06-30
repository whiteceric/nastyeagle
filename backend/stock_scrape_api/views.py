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
from django.conf import settings

import json
import os
import sys

# Load tickers
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'static/stock_scrape_api/tickers.json')
with open(filename, 'rb') as f:
    tickers = json.load(f)

def home_view(request):
    return render(request, 'home.html', {})

@api_view(['GET'])
def current_price(request, ticker):
    ticker = ticker.upper()
    force_update = request.GET.get('force-update', 'False') == 'True'
    try:
        stock = Stock.objects.get(ticker=ticker)
        if settings.DEBUG:
            print(f'Found ticker {ticker}: {stock}', flush=True)
    except Stock.DoesNotExist:
        if ticker in tickers:
            stock = Stock(ticker=ticker.upper(), name=tickers[ticker])
            if settings.DEBUG:
                print(f'Create Stock object for {ticker}: {stock}', flush=True)
        else:
            if settings.DEBUG:
                print(f'{ticker} is invalid', flush=True)
            return Response(status=status.HTTP_404_NOT_FOUND)
    stock.update(force_update=force_update)
    # stock.save()
    serializer = StockSerializer(stock, many=False)
    sys.stdout.flush()
    return Response(serializer.data)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 
