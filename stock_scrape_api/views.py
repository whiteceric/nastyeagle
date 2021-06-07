from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SymbolSerializer
from .stock_scraper import get_current_price, get_prev_week_endpoints
from datetime import datetime

import json

# create some views

@api_view(['GET'])
def current_price(request, ticker):
    try:
        price = get_current_price(ticker)
        return Response({
            'price': price, 
            'ticker': ticker,
            'time-checked': datetime.utcnow().timestamp(),
        })
    except: # add special except for the error we create in stock scraper
        return Response(status=status.HTTP_404_NOT_FOUND)

    
