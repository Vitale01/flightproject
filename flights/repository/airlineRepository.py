from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId


class AirlineRepository:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.airlines_collection = self.db['airlines']

    def get_all_airlines(self):
        return list(self.airlines_collection.find())

    def get_airline_by_id(self, airline_id):
        return self.airlines_collection.find_one({'_id': ObjectId(airline_id)})

    def create_airline(self, airline_id, name, alias, iata, callsign, country, active, icao):
        airline = {
            'airline_id': airline_id,
            'name': name,
            'alias': alias,
            'iata': iata,
            'callsign': callsign,
            'country': country,
            'active': active,
            'icao': icao,
        }
        result = self.airlines_collection.insert_one(airline)
        airline['_id'] = result.inserted_id
        return airline

    def update_airline(self, airline_id, name=None, alias=None, iata=None, callsign=None, country=None, active=None,
                       icao=None):
        update_fields = {}
        if name:
            update_fields['name'] = name
        if alias:
            update_fields['alias'] = alias
        if iata:
            update_fields['iata'] = iata
        if callsign:
            update_fields['callsign'] = callsign
        if country:
            update_fields['country'] = country
        if active:
            update_fields['active'] = active
        if icao:
            update_fields['icao'] = icao

        result = self.airlines_collection.find_one_and_update(
            {'_id': ObjectId(airline_id)},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def delete_airline(self, airline_id):
        result = self.airlines_collection.delete_one({'_id': ObjectId(airline_id)})
        return result.deleted_count > 0
