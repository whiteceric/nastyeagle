from django.urls import path, include
from .views import current_price, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('stock-price/<str:ticker>', current_price, name='stock-price'),
]
