from django.http import JsonResponse
from django.views import View
from .models import Route, Airline, Airplane, Airport
from django.shortcuts import get_object_or_404
# Airport Views
class AirportView(View):
    def get(self, request, airport_id=None):
        if airport_id:
            airport = get_object_or_404(Airport, _id=airport_id)
            data = {
                'airport': {
                    'id': str(airport._id),
                    'airport_id': airport.airport_id,
                    'name': airport.name,
                    'city': airport.city,
                    'country': airport.country,
                    'iata': airport.iata,
                    'icao': airport.icao,
                    'latitude': airport.latitude,
                    'longitude': airport.longitude,
                    'altitude': airport.altitude,
                    'timezone': airport.timezone,
                    'dst': airport.dst,
                    'db_timezone': airport.db_timezone,
                    'type': airport.type,
                    'source': airport.source,
                }
            }
        else:
            airports = Airport.objects.all()
            data = {
                'airports': list(airports.values())
            }
        return JsonResponse(data)