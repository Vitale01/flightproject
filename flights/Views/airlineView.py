from django.http import JsonResponse
from django.views import View
from flights.repository.airlineRepository import AirlineRepository
from django_request_mapping import request_mapping


@request_mapping("/airlines")
class AirlineView(View):

    def __init__(self):
        super().__init__()
        self.airline_repository = AirlineRepository(
            db_url='mongodb://localhost:27017/',  # URL del tuo database MongoDB
            db_name='Voli'  # Nome del tuo database MongoDB
        )

    @request_mapping("/getAll", method="get")
    def get_all_airlines(self, request):
        airlines = self.airline_repository.get_all_airlines()
        data = []
        for airline in airlines:
            airline_data = {
                'id': str(airline['_id']),  # Converti ObjectId in stringa per JSON
                'Airline ID': airline.get('Airline ID', ''),
                'Name': airline.get('Name', ''),
                'Alias': airline.get('Alias', ''),
                'IATA': airline.get('IATA', ''),
                'Callsign': airline.get('Callsign', ''),
                'Country': airline.get('Country', ''),
                'Active': airline.get('Active', ''),
                'ICAO': airline.get('ICAO', '')
            }
            data.append(airline_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<str:airline_id>", method="get")
    def get_airline_by_id(self, request, airline_id):
        airline = self.airline_repository.get_airline_by_id(airline_id)
        if airline:
            airline_data = {
                'id': str(airline['_id']),  # Converti ObjectId in stringa per JSON
                'Airline ID': airline.get('Airline ID', ''),
                'Name': airline.get('Name', ''),
                'Alias': airline.get('Alias', ''),
                'IATA': airline.get('IATA', ''),
                'Callsign': airline.get('Callsign', ''),
                'Country': airline.get('Country', ''),
                'Active': airline.get('Active', ''),
                'ICAO': airline.get('ICAO', ''),
            }
            return JsonResponse(airline_data)
        else:
            return JsonResponse({'error': 'Airline not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_airline(self, request):
        data = request.POST
        airline = self.airline_repository.create_airline(
            airline_id=data.get('Airline ID'),
            name=data.get('Name'),
            alias=data.get('Alias'),
            iata=data.get('IATA'),
            callsign=data.get('Callsign'),
            country=data.get('Country'),
            active=data.get('Active'),
            icao=data.get('ICAO')
        )
        return JsonResponse({
            'id': str(airline['_id']),  # Converti ObjectId in stringa per JSON
            'Airline ID': airline.get('Airline ID', ''),
            'Name': airline.get('Name', ''),
            'Alias': airline.get('Alias', ''),
            'IATA': airline.get('IATA', ''),
            'Callsign': airline.get('Callsign', ''),
            'Country': airline.get('Country', ''),
            'Active': airline.get('Active', ''),
            'ICAO': airline.get('ICAO', ''),
        })

    @request_mapping("/update/<str:objectid>", method="post")
    def update_airline(self, request, objectid):
        data = request.POST
        airline = self.airline_repository.update_airline(
            objectid = objectid,
            airline_id=data.get('Airline ID'),
            name=data.get('Name'),
            alias=data.get('Alias'),
            iata=data.get('IATA'),
            callsign=data.get('Callsign'),
            country=data.get('Country'),
            active=data.get('Active'),
            icao=data.get('ICAO')
        )
        if airline:
            return JsonResponse({
                'id': str(airline['_id']),  # Converti ObjectId in stringa per JSON
                'Airline ID': airline.get('Airline ID', ''),
                'Name': airline.get('Name', ''),
                'Alias': airline.get('Alias', ''),
                'IATA': airline.get('IATA', ''),
                'Callsign': airline.get('Callsign', ''),
                'Country': airline.get('Country', ''),
                'Active': airline.get('Active', ''),
                'ICAO': airline.get('ICAO', ''),
            })
        else:
            return JsonResponse({'error': 'Airline not found'}, status=404)

    @request_mapping("/delete/<str:objectid>", method="post")
    def delete_airline(self, request, objectid):
        result = self.airline_repository.delete_airline(objectid)
        if result:
            return JsonResponse({'message': 'Airline deleted successfully'})
        else:
            return JsonResponse({'error': 'Airline not found'}, status=404)
