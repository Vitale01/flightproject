from django.http import JsonResponse
from django.views import View
from .models import Route, Airline, Airplane, Airport
from django.shortcuts import get_object_or_404

# Route Views
class RouteView(View):
    def get(self, request, route_id=None):
        if route_id:
            route = get_object_or_404(Route, _id=route_id)
            data = {
                'route': {
                    'id': str(route._id),
                    'airline': route.airline,
                    'airline_id': route.airline_id,
                    'source_airport': route.source_airport,
                    'source_airport_id': route.source_airport_id,
                    'destination_airport': route.destination_airport,
                    'destination_airport_id': route.destination_airport_id,
                    'stops': route.stops,
                    'equipment': route.equipment,
                }
            }
        else:
            routes = Route.objects.all()
            data = {
                'routes': list(routes.values())
            }
        return JsonResponse(data)