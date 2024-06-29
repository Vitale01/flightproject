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
            'Airline ID': airline_id,
            'Name': name,
            'Alias': alias,
            'IATA': iata,
            'Callsign': callsign,
            'Country': country,
            'Active': active,
            'ICAO': icao,
        }
        result = self.airlines_collection.insert_one(airline)
        airline['_id'] = result.inserted_id
        return airline

    def update_airline(self, objectid, airline_id=None, name=None, alias=None, iata=None, callsign=None, country=None, active=None,
                       icao=None):
        update_fields = {}
        if airline_id:
            update_fields['Airline ID'] = airline_id
        if name:
            update_fields['Name'] = name
        if alias:
            update_fields['Alias'] = alias
        if iata:
            update_fields['IATA'] = iata
        if callsign:
            update_fields['Callsign'] = callsign
        if country:
            update_fields['Country'] = country
        if active:
            update_fields['Active'] = active
        if icao:
            update_fields['ICAO'] = icao

        result = self.airlines_collection.find_one_and_update(
            {'_id': ObjectId(objectid)},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def delete_airline(self, airline_id):
        result = self.airlines_collection.delete_one({'_id': ObjectId(airline_id)})
        return result.deleted_count > 0


