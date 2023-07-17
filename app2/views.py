from django.http import HttpResponse
from app2.prometheus import my_counter

def my_view(request):
    # Increment the counter
    my_counter.inc()
    # Your view logic
    return HttpResponse('')