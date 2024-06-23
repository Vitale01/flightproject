from django.http import JsonResponse
from django.views import View
from flights.repository.airportRepository import AirportRepository
from django_request_mapping import request_mapping


@request_mapping("/airports")
class AirportView(View):

    def __init__(self):
        super().__init__()
        self.airport_repository = AirportRepository(
            db_url='mongodb://localhost:27017/',  # Inserisci l'URL del tuo database MongoDB
            db_name='Voli'  # Inserisci il nome del tuo database MongoDB
        )

    @request_mapping("/getAll", method="get")
    def get_all_airports(self, request):
        airports = self.airport_repository.get_all_airports()
        data = []
        for airport in airports:
            airport_data = {
                'id': str(airport['_id']),  # Converti ObjectId in stringa per JSON
                'airline_id': airport.get('Airline ID', ''),
                'airline': airport.get('Airline', ''),
                'sourceAirport': airport.get('Source airport', ''),
                'sourceAirport_id': airport.get('Source airport ID', ''),
                'destinationAirport': airport.get('Destination airport', ''),
                'destinationAirport_id': airport.get('destinationAirport_id', ''),
                'stops': airport.get('stops', 0),
                'equipment': airport.get('equipment', '')
            }
            data.append(airport_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<uuid:airport_id>", method="get")
    def get_airport_by_id(self, request, airport_id):
        airport = self.airport_repository.get_airport_by_id(airport_id)
        if airport:
            airport_data = {
                'id': str(airport['_id']),  # Converti ObjectId in stringa per JSON
                'airline_id': airport.get('airline_id', ''),
                'airline': airport.get('airline', ''),
                'sourceAirport': airport.get('sourceAirport', ''),
                'sourceAirport_id': airport.get('sourceAirport_id', ''),
                'destinationAirport': airport.get('destinationAirport', ''),
                'destinationAirport_id': airport.get('destinationAirport_id', ''),
                'stops': airport.get('stops', 0),
                'equipment': airport.get('equipment', ''),
            }
            return JsonResponse(airport_data)
        else:
            return JsonResponse({'error': 'Airport not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_airport(self, request):
        data = request.POST
        airport = self.airport_repository.create_airport(
            airline_id=data.get('airline_id'),
            airline=data.get('airline'),
            source_airport=data.get('sourceAirport'),
            source_airport_id=data.get('sourceAirport_id'),
            destination_airport=data.get('destinationAirport'),
            destination_airport_id=data.get('destinationAirport_id'),
            stops=int(data.get('stops')),
            equipment=data.get('equipment')
        )
        return JsonResponse({
            'id': str(airport['_id']),
            'airline_id': airport.get('airline_id', ''),
            'airline': airport.get('airline', ''),
            'sourceAirport': airport.get('sourceAirport', ''),
            'sourceAirport_id': airport.get('sourceAirport_id', ''),
            'destinationAirport': airport.get('destinationAirport', ''),
            'destinationAirport_id': airport.get('destinationAirport_id', ''),
            'stops': airport.get('stops', 0),
            'equipment': airport.get('equipment', ''),
        })

    @request_mapping("/update/<uuid:airport_id>", method="post")
    def update_airport(self, request, airport_id):
        data = request.POST
        airport = self.airport_repository.update_airport(
            airport_id=airport_id,
            airline_id=data.get('airline_id'),
            airline=data.get('airline'),
            source_airport=data.get('sourceAirport'),
            source_airport_id=data.get('sourceAirport_id'),
            destination_airport=data.get('destinationAirport'),
            destination_airport_id=data.get('destinationAirport_id'),
            stops=int(data.get('stops')),
            equipment=data.get('equipment')
        )
        if airport:
            return JsonResponse({
                'id': str(airport['_id']),
                'airline_id': airport.get('airline_id', ''),
                'airline': airport.get('airline', ''),
                'sourceAirport': airport.get('sourceAirport', ''),
                'sourceAirport_id': airport.get('sourceAirport_id', ''),
                'destinationAirport': airport.get('destinationAirport', ''),
                'destinationAirport_id': airport.get('destinationAirport_id', ''),
                'stops': airport.get('stops', 0),
                'equipment': airport.get('equipment', ''),
            })
        else:
            return JsonResponse({'error': 'Airport not found'}, status=404)

    @request_mapping("/delete/<uuid:airport_id>", method="post")
    def delete_airport(self, request, airport_id):
        result = self.airport_repository.delete_airport(airport_id)
        if result:
            return JsonResponse({'message': 'Airport deleted successfully'})
        else:
            return JsonResponse({'error': 'Airport not found'}, status=404)
