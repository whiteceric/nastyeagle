from django.urls import path, include
from .views import current_price

urlpatterns = [
    path('current-price/<str:ticker>', current_price, name='current-price')
]
