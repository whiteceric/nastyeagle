from django.urls import path, include
from .views import current_price

urlpatterns = [
    path('stock-price/<str:ticker>', current_price, name='stock-price')
]
