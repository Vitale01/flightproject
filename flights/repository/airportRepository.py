from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId


class AirportRepository:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.airports_collection = self.db['airport']

    def get_all_airports(self):
        return list(self.airports_collection.find())

    def get_airport_by_id(self, airport_id):
        return self.airports_collection.find_one({'_id': ObjectId(airport_id)})

    def create_airport(self, airline_id, airline, source_airport, source_airport_id, destination_airport,
                       destination_airport_id, stops, equipment):
        airport = {
            'airline_id': airline_id,
            'airline': airline,
            'source_airport': source_airport,
            'source_airport_id': source_airport_id,
            'destination_airport': destination_airport,
            'destination_airport_id': destination_airport_id,
            'stops': stops,
            'equipment': equipment,
        }
        result = self.airports_collection.insert_one(airport)
        airport['_id'] = result.inserted_id
        return airport

    def update_airport(self, airport_id, airline_id=None, airline=None, source_airport=None, source_airport_id=None,
                       destination_airport=None, destination_airport_id=None, stops=None, equipment=None):
        update_fields = {}
        if airline_id:
            update_fields['airline_id'] = airline_id
        if airline:
            update_fields['airline'] = airline
        if source_airport:
            update_fields['source_airport'] = source_airport
        if source_airport_id:
            update_fields['source_airport_id'] = source_airport_id
        if destination_airport:
            update_fields['destination_airport'] = destination_airport
        if destination_airport_id:
            update_fields['destination_airport_id'] = destination_airport_id
        if stops:
            update_fields['stops'] = stops
        if equipment:
            update_fields['equipment'] = equipment

        result = self.airports_collection.find_one_and_update(
            {'_id': ObjectId(airport_id)},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def delete_airport(self, airport_id):
        result = self.airports_collection.delete_one({'_id': ObjectId(airport_id)})
        return result.deleted_count > 0
