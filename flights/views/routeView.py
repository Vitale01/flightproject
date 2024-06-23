from django.http import JsonResponse
from django.views import View
from flights.repository.routeRepository import RouteRepository
from django_request_mapping import request_mapping


@request_mapping("/routes")
class RouteView(View):

    def __init__(self):
        super().__init__()
        self.route_repository = RouteRepository(
            db_url='mongodb://localhost:27017/',  # Inserisci l'URL del tuo database MongoDB
            db_name='Voli'  # Inserisci il nome del tuo database MongoDB
        )

    @request_mapping("/getAll", method="get")
    def get_all_routes(self, request):
        routes = self.route_repository.get_all_routes()
        data = []
        for route in routes:
            route_data = {
                'id': str(route['_id']),  # Converti ObjectId in stringa per JSON
                'airline': route.get('Airline', ''),
                'airline_id': route.get('Airline ID', ''),
                'source_airport': route.get('Source airport', ''),
                'source_airport_id': route.get('Source airport ID', ''),
                'destination_airport': route.get('Destination airport', ''),
                'destination_airport_id': route.get('Destination airport ID', ''),
                'stops': route.get('Stops', 0),
                'equipment': route.get('Equipment', '')
            }
            data.append(route_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<uuid:route_id>", method="get")
    def get_route_by_id(self, request, route_id):
        route = self.route_repository.get_route_by_id(route_id)
        if route:
            route_data = {
                'id': str(route['_id']),  # Converti ObjectId in stringa per JSON
                'airline': route.get('Airline', ''),
                'airline_id': route.get('Airline ID', ''),
                'source_airport': route.get('Source airport', ''),
                'source_airport_id': route.get('Source airport ID', ''),
                'destination_airport': route.get('Destination airport', ''),
                'destination_airport_id': route.get('Destination airport ID', ''),
                'stops': route.get('Stops', 0),
                'equipment': route.get('Equipment', '')
            }
            return JsonResponse(route_data)
        else:
            return JsonResponse({'error': 'Route not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_route(self, request):
        data = request.POST
        route = self.route_repository.create_route(
            airline=data.get('Airline'),
            airline_id=data.get('Airline ID'),
            source_airport=data.get('Source airport'),
            source_airport_id=data.get('Source airport ID'),
            destination_airport=data.get('Destination airport'),
            destination_airport_id=data.get('Destination airport ID'),
            stops=int(data.get('Stops')),
            equipment=data.get('Equipment')
        )
        return JsonResponse({
                'id': str(route['_id']),  # Converti ObjectId in stringa per JSON
                'airline': route.get('Airline', ''),
                'airline_id': route.get('Airline ID', ''),
                'source_airport': route.get('Source airport', ''),
                'source_airport_id': route.get('Source airport ID', ''),
                'destination_airport': route.get('Destination airport', ''),
                'destination_airport_id': route.get('Destination airport ID', ''),
                'stops': route.get('Stops', 0),
                'equipment': route.get('Equipment', '')
        })

    @request_mapping("/update/<uuid:route_id>", method="post")
    def update_route(self, request, route_id):
        data = request.POST
        route = self.route_repository.update_route(
            route_id=route_id,
            airline=data.get('Airline'),
            airline_id=data.get('Airline ID'),
            source_airport=data.get('Source airport'),
            source_airport_id=data.get('Source airport ID'),
            destination_airport=data.get('Destination airport'),
            destination_airport_id=data.get('Destination airport ID'),
            stops=int(data.get('Stops')),
            equipment=data.get('Equipment')
        )
        if route:
            return JsonResponse({
                'id': str(route['_id']),  # Converti ObjectId in stringa per JSON
                'airline': route.get('Airline', ''),
                'airline_id': route.get('Airline ID', ''),
                'source_airport': route.get('Source airport', ''),
                'source_airport_id': route.get('Source airport ID', ''),
                'destination_airport': route.get('Destination airport', ''),
                'destination_airport_id': route.get('Destination airport ID', ''),
                'stops': route.get('Stops', 0),
                'equipment': route.get('Equipment', '')
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
