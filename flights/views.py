from django.shortcuts import render
from django.http import JsonResponse
# Create your Views here.
# flights/Views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Route


def index(request):
    return render(request, 'index.html')


def servizi(request):
    return render(request, 'Servizi.html')


def get_subcategories(request):
    main_category = request.GET.get('main_category')
    subcategories = {
        'airlines': ['getAll', 'getAirlineForCountry', 'getActiveAirlines'],
        'airplanes': ['getAll'],
        'airports': ['getAll', 'matching_codes', 'airports_by_country', 'get_cities_with_most_airports'],
        'routes': ['getAll', 'statistics_routes', 'max_stops']
    }

    return JsonResponse(subcategories.get(main_category, []), safe=False)
