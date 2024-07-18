import json

from django.http import JsonResponse
from django.views import View
from flights.repository.airportRepository import AirportRepository
from flights.repository.airplaneRepository import AirplaneRepository
from django_request_mapping import request_mapping
from bson import ObjectId


@request_mapping("/airports")
class AirportView(View):

    def __init__(self):
        super().__init__()
        self.airport_repository = AirportRepository(
            db_url='mongodb://localhost:27017/',
            db_name='Voli'
        )
        self.airplane_repository = AirplaneRepository(
            db_url='mongodb://localhost:27017/', db_name='Voli'
        )

    @request_mapping("/getAll", method="get")
    def get_all_airports(self, request):
        airports = self.airport_repository.get_all_airports()
        data = []
        for airport in airports:
            airport_data = {
                'id': str(airport['_id']),  # Converti ObjectId in stringa per JSON
                'Airport ID': airport.get('Airport ID', ''),
                'Name': airport.get('Name', ''),
                'City': airport.get('City', ''),
                'Country': airport.get('Country', ''),
                'IATA': airport.get('IATA', ''),
                'ICAO': airport.get('ICAO', ''),
                'Latitudine': airport.get('Latitude', ''),
                'Longitudine': airport.get('Longitude', ''),
                'Altitude': airport.get('Altitude', ''),
                'Timezone': airport.get('Timezone', ''),
                'DST': airport.get('DST', ''),
                'Tz database time zone': airport.get('Tz database time zone', ''),
                'Type': airport.get('Type', ''),
                'Source': airport.get('Source', '')
            }
            data.append(airport_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<str:airport_id>", method="get")
    def get_airport_by_id(self, request, airport_id):
        airport = self.airport_repository.get_airport_by_id(airport_id)
        if airport:
            airport_data = {
                'id': str(airport['_id']),  # Converti ObjectId in stringa per JSON
                'Airport ID': airport.get('Airport ID', ''),
                'Name': airport.get('Name', ''),
                'City': airport.get('City', ''),
                'Country': airport.get('Country', ''),
                'IATA': airport.get('IATA', ''),
                'ICAO': airport.get('ICAO', ''),
                'Latitudine': airport.get('Latitude', ''),
                'Longitudine': airport.get('Longitude', ''),
                'Altitude': airport.get('Altitude', ''),
                'Timezone': airport.get('Timezone', ''),
                'DST': airport.get('DST', ''),
                'Tz database time zone': airport.get('Tz database time zone', ''),
                'Type': airport.get('Type', ''),
                'Source': airport.get('Source', '')
            }
            return JsonResponse(airport_data)
        else:
            return JsonResponse({'error': 'Airport not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_airport(self, request):
        data = request.POST
        airport = self.airport_repository.create_airport(
            airport_id=data.get('Airport ID'),
            name=data.get('Name'),
            city=data.get('City'),
            country=data.get('Country'),
            iata=data.get('IATA'),
            icao=data.get('ICAO'),
            latitudine=data.get('Latitudine'),
            longitudine=data.get('Longitudine'),
            altitude=data.get('Altitude'),
            timezone=data.get('Timezone'),
            dst=data.get('DST'),
            tz_database_timezone=data.get('Tz database time zone'),
            type=data.get('Type'),
            source=data.get('Source')
        )
        return JsonResponse({
            'id': str(airport['_id']),
            'Airport ID': airport.get('Airport ID', ''),
            'Name': airport.get('Name', ''),
            'City': airport.get('City', ''),
            'Country': airport.get('Country', ''),
            'IATA': airport.get('IATA', ''),
            'ICAO': airport.get('ICAO', ''),
            'Latitudine': airport.get('Latitude', ''),
            'Longitudine': airport.get('Longitude', ''),
            'Altitude': airport.get('Altitude', ''),
            'Timezone': airport.get('Timezone', ''),
            'DST': airport.get('DST', ''),
            'Tz database time zone': airport.get('Tz database time zone', ''),
            'Type': airport.get('Type', ''),
            'Source': airport.get('Source', '')
        })

    @request_mapping("/update/<str:airport_id>", method="post")
    def update_airport(self, request, airport_id):
        data = request.POST
        airport = self.airport_repository.update_airport(
            airport_id=airport_id,
            name=data.get('Name'),
            city=data.get('City'),
            country=data.get('Country'),
            iata=data.get('IATA'),
            icao=data.get('ICAO'),
            latitudine=data.get('Latitudine'),
            longitudine=data.get('Longitudine'),
            altitude=data.get('Altitude'),
            timezone=data.get('Timezone'),
            dst=data.get('DST'),
            tz_database_timezone=data.get('Tz database time zone'),
            type=data.get('Type'),
            source=data.get('Source')
        )
        if airport:
            return JsonResponse({
                'id': str(airport['_id']),
                'Airport ID': airport.get('Airport ID', ''),
                'Name': airport.get('Name', ''),
                'City': airport.get('City', ''),
                'Country': airport.get('Country', ''),
                'IATA': airport.get('IATA', ''),
                'ICAO': airport.get('ICAO', ''),
                'Latitudine': airport.get('Latitude', ''),
                'Longitudine': airport.get('Longitude', ''),
                'Altitude': airport.get('Altitude', ''),
                'Timezone': airport.get('Timezone', ''),
                'DST': airport.get('DST', ''),
                'Tz database time zone': airport.get('Tz database time zone', ''),
                'Type': airport.get('Type', ''),
                'Source': airport.get('Source', '')
            })
        else:
            return JsonResponse({'error': 'Airport not found'}, status=404)

    @request_mapping("/delete/<str:airport_id>", method="post")
    def delete_airport(self, request, airport_id):
        result = self.airport_repository.delete_airport(airport_id)
        if result:
            return JsonResponse({'message': 'Airport deleted successfully'})
        else:
            return JsonResponse({'error': 'Airport not found'}, status=404)

    @request_mapping("/get_cities_with_most_airports", method="get")
    def get_cities(self, request):
        cities_with_most_airports = self.airport_repository.get_cities_with_most_airports()
        response = [
            {
                'city': city['_id'],
                'count': city['count']
            } for city in cities_with_most_airports
        ]
        return JsonResponse(response, safe=False)

    @request_mapping("/airports_by_country", method="get")
    def get_airports_by_country(self, request):
        airports_by_country = self.airport_repository.get_airports_by_country()
        response = [{
            'country': airport['_id'],
            'total_airports': airport['total_airports']
        } for airport in airports_by_country]

        return JsonResponse(response, safe=False)

    # Questa funzione serve per la stampa degli ObjectID
    def convert_object_id_to_str(self, data):
        if isinstance(data, dict):
            return {k: self.convert_object_id_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_object_id_to_str(item) for item in data]
        elif isinstance(data, ObjectId):
            return str(data)
        else:
            return data

    @request_mapping("/matching_codes", method="get")
    def get_matching_codes(self, request):
        airports = self.airport_repository.get_all_airports()
        airplanes = self.airplane_repository.get_all_airplanes()

        airport_iata_map = {airport['IATA']: airport for airport in airports if 'IATA' in airport}
        airplane_iata_map = {airplane['IATA code']: airplane for airplane in airplanes if 'IATA code' in airplane}

        airport_icao_map = {airport['ICAO']: airport for airport in airports if 'ICAO' in airport}
        airplane_icao_map = {airplane['ICAO code']: airplane for airplane in airplanes if 'ICAO code' in airplane}

        matching_codes = []
        for iata, airport in airport_iata_map.items():
            if iata in airplane_iata_map:
                matching_codes.append({
                    'code': iata,
                    'type': 'iata',
                    'airport': json.dumps(self.convert_object_id_to_str(airport)),
                    'airplane': json.dumps(self.convert_object_id_to_str(airplane_iata_map[iata]))
                })

        for icao, airport in airport_icao_map.items():
            if icao in airplane_icao_map:
                matching_codes.append({
                    'code': icao,
                    'type': 'icao',
                    'airport': json.dumps(self.convert_object_id_to_str(airport)),
                    'airplane': json.dumps(self.convert_object_id_to_str(airplane_icao_map[icao]))
                })

        return JsonResponse(matching_codes, safe=False)

    def convert_object_id_to_str(self, obj):
        # Assicurati che obj sia un dizionario JSON serializzabile
        if isinstance(obj, dict):
            return str(obj.get('_id', ''))
        return str(obj)

