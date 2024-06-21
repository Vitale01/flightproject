from django.shortcuts import render

# Create your views here.
# flights/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Route


@api_view(['GET'])
def frequent_flights(request):
    start_year = int(request.GET.get('start_year'))
    end_year = int(request.GET.get('end_year'))

    flights = Route.objects.filter(
        departure_date__year__gte=start_year,
        departure_date__year__lte=end_year
    ).values('destination_airport').annotate(count=Count('destination_airport')).order_by('-count')[:10]

    return Response(flights)
