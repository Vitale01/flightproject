from django.http import JsonResponse
from django.views import View
from flights.repository.routeRepository import RouteRepository
from django_request_mapping import request_mapping


@request_mapping("/routes")
class RouteView(View):

    def __init__(self):
        super().__init__()
        self.route_repository = RouteRepository(
            db_url='mongodb://localhost:27017/',
            db_name='Voli'
        )

    @request_mapping("/getAll", method="get")
    def get_all_routes(self, request):
        routes = self.route_repository.get_all_routes()
        data = []
        for route in routes:
            route_data = {
                'id': str(route['_id']),
                'Airline': route.get('Airline', ''),
                'Airline ID': route.get('Airline ID', ''),
                'Source airport': route.get('Source airport', ''),
                'Source airport ID': route.get('Source airport ID', ''),
                'Destination airport': route.get('Destination airport', ''),
                'Destination airport ID': route.get('Destination airport ID', ''),
                'Stops': route.get('Stops', 0),
                'Equipment': route.get('Equipment', '')
            }
            data.append(route_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<str:route_id>", method="get")
    def get_route_by_id(self, request, route_id):
        route = self.route_repository.get_route_by_id(route_id)
        if route:
            route_data = {
                'id': str(route['_id']),
                'Airline': route.get('Airline', ''),
                'Airline ID': route.get('Airline ID', ''),
                'Source airport': route.get('Source airport', ''),
                'Source airport ID': route.get('Source airport ID', ''),
                'Destination airport': route.get('Destination airport', ''),
                'Destination airport ID': route.get('Destination airport ID', ''),
                'Stops': route.get('Stops', 0),
                'Equipment': route.get('Equipment', '')
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
                'id': str(route['_id']),
                'Airline': route.get('Airline', ''),
                'Airline ID': route.get('Airline ID', ''),
                'Source airport': route.get('Source airport', ''),
                'Source airport ID': route.get('Source airport ID', ''),
                'Destination airport': route.get('Destination airport', ''),
                'Destination airport ID': route.get('Destination airport ID', ''),
                'Stops': route.get('Stops', 0),
                'Equipment': route.get('Equipment', '')
        })

    @request_mapping("/update/<str:route_id>", method="post")
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
                'id': str(route['_id']),
                'Airline': route.get('Airline', ''),
                'Airline ID': route.get('Airline ID', ''),
                'Source airport': route.get('Source airport', ''),
                'Source airport ID': route.get('Source airport ID', ''),
                'Destination airport': route.get('Destination airport', ''),
                'Destination airport ID': route.get('Destination airport ID', ''),
                'Stops': route.get('Stops', 0),
                'Equipment': route.get('Equipment', '')
            })
        else:
            return JsonResponse({'error': 'Route not found'}, status=404)

    @request_mapping("/delete/<str:route_id>", method="post")
    def delete_route(self, request, route_id):
        result = self.route_repository.delete_route(route_id)
        if result:
            return JsonResponse({'message': 'Route deleted successfully'})
        else:
            return JsonResponse({'error': 'Route not found'}, status=404)

    @request_mapping("/statistics_routes", method="get")
    def get_route_statistics(self, request):
        route_statistics = self.route_repository.get_route_statistics()
        response = [{
            'airline': stat['airline'],
            'total_routes': stat['total_routes']
        } for stat in route_statistics]

        return JsonResponse(response, safe=False)

    @request_mapping("/max_stops", method="get")
    def get_routes_with_max_stops(self, request):
        routes = self.route_repository.get_all_routes()
        max_stops = max(route.get('Stops', 0) for route in routes)
        routes_with_max_stops = [
            {
                'id': str(route['_id']),
                'Airline': route.get('Airline', ''),
                'Airline ID': route.get('Airline ID', ''),
                'Source airport': route.get('Source airport', ''),
                'Source airport ID': route.get('Source airport ID', ''),
                'Destination airport': route.get('Destination airport', ''),
                'Destination airport ID': route.get('Destination airport ID', ''),
                'Stops': route.get('Stops', 0),
                'Equipment': route.get('Equipment', '')
            }
            for route in routes if route.get('Stops', 0) == max_stops
        ]

        return JsonResponse(routes_with_max_stops, safe=False)
