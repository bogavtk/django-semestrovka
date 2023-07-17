from django.urls import path, include

from app2.views import my_view

urlpatterns = [
    path('prometheus-xyzabc/metrics/', my_view)
]
