from flights.repository.airplaneRepository import AirplaneRepository
from django.http import JsonResponse
from django.views import View
from django_request_mapping import request_mapping

@request_mapping("/airplanes")
class AirplaneView(View):

    def __init__(self):
        super().__init__()
        self.airplane_repository: AirplaneRepository = AirplaneRepository(
            db_url='mongodb://localhost:27017/',  # URL del tuo database MongoDB
            db_name='Voli'  # Nome del tuo database MongoDB
        )

    @request_mapping("/getAll", method="get")
    def get_all_airplanes(self, request):
        airplanes = self.airplane_repository.get_all_airplanes()
        data = []
        for airplane in airplanes:
            airplane_data = {
                'id': str(airplane['_id']),  # Converti ObjectId in stringa per JSON
                'Name': airplane.get('Name', ''),
                'IATA code': airplane.get('IATA code', ''),
                'ICAO code': airplane.get('ICAO code', '')
            }
            data.append(airplane_data)

        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<str:airplane_id>", method="get")
    def get_airplane_by_id(self, request, airplane_id):
        airplane = self.airplane_repository.get_airplane_by_id(airplane_id)
        if airplane:
            airplane_data = {
                'id': str(airplane['_id']),  # Converti ObjectId in stringa per JSON
                'Name': airplane.get('Name', ''),
                'IATA code': airplane.get('IATA code', ''),
                'ICAO code': airplane.get('ICAO code', '')
            }
            return JsonResponse(airplane_data)
        else:
            return JsonResponse({'error': 'Airplane not found'}, status=404)

    @request_mapping("/create", method="post")
    def create_airplane(self, request):
        data = request.POST
        airplane = self.airplane_repository.create_airplane(
            name=data.get('Name'),
            iata_code=data.get('IATA code'),
            icao_code=data.get('ICAO code')
        )
        return JsonResponse({
            'id': str(airplane['_id']),  # Converti ObjectId in stringa per JSON
            'Name': airplane.get('Name', ''),
            'IATA code': airplane.get('IATA code', ''),
            'ICAO code': airplane.get('ICAO code', '')
        })

    @request_mapping("/update/<str:airplane_id>", method="post")
    def update_airplane(self, request, airplane_id):
        data = request.POST
        airplane = self.airplane_repository.update_airplane(
            airplane_id=airplane_id,
            name=data.get('Name'),
            iata_code=data.get('IATA code'),
            icao_code=data.get('ICAO code')
        )
        if airplane:
            return JsonResponse({
                'id': str(airplane['_id']),  # Converti ObjectId in stringa per JSON
                'Name': airplane.get('Name', ''),
                'IATA code': airplane.get('IATA code', ''),
                'ICAO code': airplane.get('ICAO code', '')
            })
        else:
            return JsonResponse({'error': 'Airplane not found'}, status=404)

    @request_mapping("/delete/<str:airplane_id>", method="post")
    def delete_airplane(self, request, airplane_id):
        result = self.airplane_repository.delete_airplane(airplane_id)
        if result:
            return JsonResponse({'message': 'Airplane deleted successfully'})
        else:
            return JsonResponse({'error': 'Airplane not found'}, status=404)
