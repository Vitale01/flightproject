from django.http import JsonResponse
from django.views import View
from .models import Route, Airline, Airplane, Airport
from django.shortcuts import get_object_or_404
# Airplane Views
class AirplaneView(View):
    def get(self, request, airplane_id=None):
        if airplane_id:
            airplane = get_object_or_404(Airplane, _id=airplane_id)
            data = {
                'airplane': {
                    'id': str(airplane._id),
                    'name': airplane.name,
                    'iata_code': airplane.iata_code,
                    'icao_code': airplane.icao_code,
                }
            }
        else:
            airplanes = Airplane.objects.all()
            data = {
                'airplanes': list(airplanes.values())
            }
        return JsonResponse(data)