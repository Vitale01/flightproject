from django.http import JsonResponse
from django.views import View
from flightproject.flightproject.flights.repository.routeRepository import RouteRepository
from django_request_mapping import request_mapping


@request_mapping("/routes")
class RouteView(View):

    def __init__(self):
        super().__init__()
        self.route_repository = RouteRepository(
            db_url='mongodb://localhost:27017/',  # Inserisci l'URL del tuo database MongoDB
            db_name='flights'  # Inserisci il nome del tuo database MongoDB
        )

    @request_mapping("/getAll", method="get")
    def get_all_routes(self, request):
        routes = self.route_repository.get_all_routes()
        data = []
        for route in routes:
            route_data = {
                'id': str(route['_id']),  # Converti ObjectId in stringa per JSON
                'airline': route.get('airline', ''),
                'airline_id': route.get('airline_id', ''),
                'source_airport': route.get('source_airport', ''),
                'source_airport_id': route.get('source_airport_id', ''),
                'destination_airport': route.get('destination_airport', ''),
                'destination_airport_id': route.get('destination_airport_id', ''),
                'stops': route.get('stops', 0),
                'equipment': route.get('equipment', ''),
            }
            data.append(route_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<uuid:route_id>", method="get")
    def get_route_by_id(self, request, route_id):
        route = self.route_repository.get_route_by_id(route_id)
        if route:
            route_data = {
                'id': str(route['_id']),  # Converti ObjectId in stringa per JSON
                'airline': route.get('airline', ''),
                'airline_id': route.get('airline_id', ''),
                'source_airport': route.get('source_airport', ''),
                'source_airport_id': route.get('source_airport_id', ''),
                'destination_airport': route.get('destination_airport', ''),
                'destination_airport_id': route.get('destination_airport_id', ''),
                'stops': route.get('stops', 0),
                'equipment': route.get('equipment', ''),
            }
            return JsonResponse(route_data)
        else:
            return JsonResponse({'error': 'Route not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_route(self, request):
        data = request.POST
        route = self.route_repository.create_route(
            airline=data.get('airline'),
            airline_id=data.get('airline_id'),
            source_airport=data.get('source_airport'),
            source_airport_id=data.get('source_airport_id'),
            destination_airport=data.get('destination_airport'),
            destination_airport_id=data.get('destination_airport_id'),
            stops=int(data.get('stops')),
            equipment=data.get('equipment')
        )
        return JsonResponse({
            'id': str(route['_id']),
            'airline': route.get('airline', ''),
            'airline_id': route.get('airline_id', ''),
            'source_airport': route.get('source_airport', ''),
            'source_airport_id': route.get('source_airport_id', ''),
            'destination_airport': route.get('destination_airport', ''),
            'destination_airport_id': route.get('destination_airport_id', ''),
            'stops': route.get('stops', 0),
            'equipment': route.get('equipment', ''),
        })

    @request_mapping("/update/<uuid:route_id>", method="post")
    def update_route(self, request, route_id):
        data = request.POST
        route = self.route_repository.update_route(
            route_id=route_id,
            airline=data.get('airline'),
            airline_id=data.get('airline_id'),
            source_airport=data.get('source_airport'),
            source_airport_id=data.get('source_airport_id'),
            destination_airport=data.get('destination_airport'),
            destination_airport_id=data.get('destination_airport_id'),
            stops=int(data.get('stops')),
            equipment=data.get('equipment')
        )
        if route:
            return JsonResponse({
                'id': str(route['_id']),
                'airline': route.get('airline', ''),
                'airline_id': route.get('airline_id', ''),
                'source_airport': route.get('source_airport', ''),
                'source_airport_id': route.get('source_airport_id', ''),
                'destination_airport': route.get('destination_airport', ''),
                'destination_airport_id': route.get('destination_airport_id', ''),
                'stops': route.get('stops', 0),
                'equipment': route.get('equipment', ''),
            })
        else:
            return JsonResponse({'error': 'Route not found'}, status=404)

    @request_mapping("/delete/<uuid:route_id>", method="post")
    def delete_route(self, request, route_id):
        result = self.route_repository.delete_route(route_id)
        if result:
            return JsonResponse({'message': 'Route deleted successfully'})
        else:
            return JsonResponse({'error': 'Route not found'}, status=404)
