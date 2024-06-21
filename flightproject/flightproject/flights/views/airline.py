from django.http import JsonResponse
from django.views import View
from .models import Route, Airline, Airplane, Airport
from django.shortcuts import get_object_or_404
# Airline Views
class AirlineView(View):
    def get(self, request, airline_id=None):
        if airline_id:
            airline = get_object_or_404(Airline, _id=airline_id)
            data = {
                'airline': {
                    'id': str(airline._id),
                    'airline_id': airline.airline_id,
                    'name': airline.name,
                    'alias': airline.alias,
                    'iata': airline.iata,
                    'callsign': airline.callsign,
                    'country': airline.country,
                    'active': airline.active,
                    'icao': airline.icao,
                }
            }
        else:
            airlines = Airline.objects.all()
            data = {
                'airlines': list(airlines.values())
            }
        return JsonResponse(data)