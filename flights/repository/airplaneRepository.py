from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId


class AirplaneRepository:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.airplanes_collection = self.db['airplanes']

    def get_all_airplanes(self):
        return list(self.airplanes_collection.find())

    def get_airplane_by_id(self, airplane_id):
        return self.airplanes_collection.find_one({'_id': ObjectId(airplane_id)})

    def create_airplane(self, name, iata_code, icao_code):
        airplane = {
            'name': name,
            'iata_code': iata_code,
            'icao_code': icao_code,
        }
        result = self.airplanes_collection.insert_one(airplane)
        airplane['_id'] = result.inserted_id
        return airplane

    def update_airplane(self, airplane_id, name=None, iata_code=None, icao_code=None):
        update_fields = {}
        if name:
            update_fields['name'] = name
        if iata_code:
            update_fields['iURLata_code'] = iata_code
        if icao_code:
            update_fields['icao_code'] = icao_code

        result = self.airplanes_collection.find_one_and_update(
            {'_id': ObjectId(airplane_id)},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def delete_airplane(self, airplane_id):
        result = self.airplanes_collection.delete_one({'_id': ObjectId(airplane_id)})
        return result.deleted_count > 0
