from django.contrib import admin
from django.urls import path, include

from app1.views import *

urlpatterns = [
    path('create_restaurant/', RestaurantAPIView.as_view()),
    path('menu/', MenuAPIView.as_view()),
    path('promotions/', PromotionsAPIView.as_view()),
    path('increase_balance', IncreaseBalanceAPIView.as_view()),
]
