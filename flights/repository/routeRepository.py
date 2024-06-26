from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from flights.models import Route


class RouteRepository:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.routes_collection = self.db['routes']

    def get_all_routes(self):
        return list(self.routes_collection.find())

    def get_route_by_id(self, route_id):
        return self.routes_collection.find_one({'_id': ObjectId(route_id)})

    def create_route(self, airline, airline_id, source_airport, source_airport_id, destination_airport,
                     destination_airport_id, stops, equipment):
        route = {
            'Airline': airline,
            'Airline ID': airline_id,
            'Source airport': source_airport,
            'Source airport ID': source_airport_id,
            'Destination airport': destination_airport,
            'Destination airport ID': destination_airport_id,
            'Stops': stops,
            'Equipment': equipment,
        }
        result = self.routes_collection.insert_one(route)
        route['_id'] = result.inserted_id
        return route

    def update_route(self, route_id, airline=None, airline_id=None, source_airport=None, source_airport_id=None,
                     destination_airport=None, destination_airport_id=None, stops=None, equipment=None):
        update_fields = {}
        if airline:
            update_fields['Airline'] = airline
        if airline_id:
            update_fields['Airline ID'] = airline_id
        if source_airport:
            update_fields['Source airport'] = source_airport
        if source_airport_id:
            update_fields['Source airport ID'] = source_airport_id
        if destination_airport:
            update_fields['Destination airport'] = destination_airport
        if destination_airport_id:
            update_fields['Destination airport ID'] = destination_airport_id
        if stops:
            update_fields['Stops'] = stops
        if equipment:
            update_fields['Equipment'] = equipment

        result = self.routes_collection.find_one_and_update(
            {'_id': ObjectId(route_id)},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def delete_route(self, route_id):
        result = self.routes_collection.delete_one({'_id': ObjectId(route_id)})
        return result.deleted_count > 0

    def get_route_statistics(self):
        pipeline = [
            {"$group": {"_id": "$Airline", "total_routes": {"$sum": 1}}}
        ]
        statistics = list(self.routes_collection.aggregate(pipeline))
        result = []
        for stat in statistics:
            result.append({
                'airline': stat['_id'],
                'total_routes': stat['total_routes']
            })

        return result
