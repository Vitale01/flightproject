from django.http import JsonResponse
from django.views import View
from flightproject.flightproject.flights.repository.airlineRepository import AirlineRepository
from django_request_mapping import request_mapping

@request_mapping("/airlines")
class AirlineView(View):

    def __init__(self):
        super().__init__()
        self.airline_repository = AirlineRepository(
            db_url='mongodb://localhost:27017/',  # Inserisci l'URL del tuo database MongoDB
            db_name='flights'  # Inserisci il nome del tuo database MongoDB
        )

    @request_mapping("/getAll", method="get")
    def get_all_airlines(self, request):
        airlines = self.airline_repository.get_all_airlines()
        data = []
        for airline in airlines:
            airline_data = {
                'id': str(airline['_id']),  # Converti ObjectId in stringa per JSON
                'airline_id': airline.get('airline_id', ''),
                'name': airline.get('name', ''),
                'alias': airline.get('alias', ''),
                'iata': airline.get('iata', ''),
                'callsign': airline.get('callsign', ''),
                'country': airline.get('country', ''),
                'active': airline.get('active', ''),
                'icao': airline.get('icao', ''),
            }
            data.append(airline_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<uuid:airline_id>", method="get")
    def get_airline_by_id(self, request, airline_id):
        airline = self.airline_repository.get_airline_by_id(airline_id)
        if airline:
            airline_data = {
                'id': str(airline['_id']),  # Converti ObjectId in stringa per JSON
                'airline_id': airline.get('airline_id', ''),
                'name': airline.get('name', ''),
                'alias': airline.get('alias', ''),
                'iata': airline.get('iata', ''),
                'callsign': airline.get('callsign', ''),
                'country': airline.get('country', ''),
                'active': airline.get('active', ''),
                'icao': airline.get('icao', ''),
            }
            return JsonResponse(airline_data)
        else:
            return JsonResponse({'error': 'Airline not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_airline(self, request):
        data = request.POST
        airline = self.airline_repository.create_airline(
            airline_id=int(data.get('airline_id')),
            name=data.get('name'),
            alias=data.get('alias'),
            iata=data.get('iata'),
            callsign=data.get('callsign'),
            country=data.get('country'),
            active=data.get('active'),
            icao=data.get('icao')
        )
        return JsonResponse({
            'id': str(airline['_id']),
            'airline_id': airline.get('airline_id', ''),
            'name': airline.get('name', ''),
            'alias': airline.get('alias', ''),
            'iata': airline.get('iata', ''),
            'callsign': airline.get('callsign', ''),
            'country': airline.get('country', ''),
            'active': airline.get('active', ''),
            'icao': airline.get('icao', ''),
        })

    @request_mapping("/update/<uuid:airline_id>", method="post")
    def update_airline(self, request, airline_id):
        data = request.POST
        airline = self.airline_repository.update_airline(
            airline_id=airline_id,
            name=data.get('name'),
            alias=data.get('alias'),
            iata=data.get('iata'),
            callsign=data.get('callsign'),
            country=data.get('country'),
            active=data.get('active'),
            icao=data.get('icao')
        )
        if airline:
            return JsonResponse({
                'id': str(airline['_id']),
                'airline_id': airline.get('airline_id', ''),
                'name': airline.get('name', ''),
                'alias': airline.get('alias', ''),
                'iata': airline.get('iata', ''),
                'callsign': airline.get('callsign', ''),
                'country': airline.get('country', ''),
                'active': airline.get('active', ''),
                'icao': airline.get('icao', ''),
            })
        else:
            return JsonResponse({'error': 'Airline not found'}, status=404)

    @request_mapping("/delete/<uuid:airline_id>", method="post")
    def delete_airline(self, request, airline_id):
        result = self.airline_repository.delete_airline(airline_id)
        if result:
            return JsonResponse({'message': 'Airline deleted successfully'})
        else:
            return JsonResponse({'error': 'Airline not found'}, status=404)
