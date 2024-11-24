from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg
from store.models import Product


# Create your views here.
def say_hello(request):
    query_set = Product.objects.filter(collection__id__gte=0)

    return render(request, 'hello.html', {'name': 'Aziz', 'products': list(query_set)})
