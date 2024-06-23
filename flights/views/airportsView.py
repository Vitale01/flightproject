from django.http import JsonResponse
from django.views import View
from flights.repository.airportRepository import AirportRepository
from django_request_mapping import request_mapping

@request_mapping("/airports")
class AirportView(View):

    def __init__(self):
        super().__init__()
        self.airport_repository = AirportRepository(
            db_url='mongodb://localhost:27017/',  # URL del tuo database MongoDB
            db_name='Voli'  # Nome del tuo database MongoDB
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
                'Latitudine': airport.get('Latitudine', ''),
                'Longitudine': airport.get('Longitudine', ''),
                'Altitude': airport.get('Altitude', ''),
                'Timezone': airport.get('Timezone', ''),
                'DST': airport.get('DST', ''),
                'Tz database time zone': airport.get('Tz database time zone', ''),
                'Type': airport.get('Type', ''),
                'Source': airport.get('Source', '')
            }
            data.append(airport_data)
        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<uuid:airport_id>", method="get")
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
                'Latitudine': airport.get('Latitudine', ''),
                'Longitudine': airport.get('Longitudine', ''),
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
            'Latitudine': airport.get('Latitudine', ''),
            'Longitudine': airport.get('Longitudine', ''),
            'Altitude': airport.get('Altitude', ''),
            'Timezone': airport.get('Timezone', ''),
            'DST': airport.get('DST', ''),
            'Tz database time zone': airport.get('Tz database time zone', ''),
            'Type': airport.get('Type', ''),
            'Source': airport.get('Source', '')
        })

    @request_mapping("/update/<uuid:airport_id>", method="post")
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
                'Latitudine': airport.get('Latitudine', ''),
                'Longitudine': airport.get('Longitudine', ''),
                'Altitude': airport.get('Altitude', ''),
                'Timezone': airport.get('Timezone', ''),
                'DST': airport.get('DST', ''),
                'Tz database time zone': airport.get('Tz database time zone', ''),
                'Type': airport.get('Type', ''),
                'Source': airport.get('Source', '')
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
