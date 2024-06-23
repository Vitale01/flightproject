
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
                'id': str(airplane['_id']),
                'name': airplane.get('Name', ''),
                'iata_code': airplane.get('IATA code', ''),
                'icao_code': airplane.get('ICAO code', '')
            }
            data.append(airplane_data)

        return JsonResponse(data, safe=False)

    @request_mapping("/getById/<uuid:airplane_id>", method="get")
    def get_airplane_by_id(self, request, airplane_id):
        airplane = self.airplane_repository.get_airplane_by_id(airplane_id)
        data = {
            'id': str(airplane['_id']),
            'name': airplane.get('name', ''),
            'iata_type': airplane.get('iata_type', ''),
            'icao_type': airplane.get('icao_type', ''),
            'iata_code': airplane.get('iata_code', ''),
            'icao_code': airplane.get('icao_code', ''),
            'manufacturer': airplane.get('manufacturer', ''),
            'model': airplane.get('model', ''),
            'wake_category': airplane.get('wake_category', '')
        }
        return JsonResponse(data)

    @request_mapping("/create/", method="post")
    def create_airplane(self, request):
        data = request.POST
        airplane = self.airplane_repository.create_airplane(
            data.get('name'),
            data.get('iata_type'),
            data.get('icao_type')
        )
        return JsonResponse({
            'id': str(airplane['_id']),
            'name': airplane.get('name', ''),
            'iata_type': airplane.get('iata_type', ''),
            'icao_type': airplane.get('icao_type', ''),
            'iata_code': airplane.get('iata_code', ''),
            'icao_code': airplane.get('icao_code', ''),
        })

    @request_mapping("/update/<uuid:airplane_id>", method="post")
    def update_airplane(self, request, airplane_id):
        data = request.POST
        airplane = self.airplane_repository.update_airplane(
            airplane_id,
            name=data.get('name'),
            iata_code=data.get('iata_code'),
            icao_code=data.get('icao_code')
        )
        return JsonResponse({
            'id': str(airplane['_id']),
            'name': airplane.get('name', ''),
            'iata_type': airplane.get('iata_type', ''),
            'icao_type': airplane.get('icao_type', ''),
            'iata_code': airplane.get('iata_code', ''),
            'icao_code': airplane.get('icao_code', ''),
        })

    @request_mapping("/delete/<uuid:airplane_id>", method="post")
    def delete_airplane(self, request, airplane_id):
        self.airplane_repository.delete_airplane(airplane_id)
        return JsonResponse({"message": "Aereo eliminato"})
