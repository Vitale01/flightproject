from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId


class AirportRepository:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.airports_collection = self.db['airports']

    def get_all_airports(self):
        return list(self.airports_collection.find())

    def get_airport_by_id(self, airport_id):
        return self.airports_collection.find_one({'_id': ObjectId(airport_id)})

    def create_airport(self, airport_id, name, city, country, iata, icao, latitudine, longitudine, altitude,
                       timezone, dst, tz_database_timezone, type, source):
        airport = {
            'Airport ID': airport_id,
            'Name': name,
            'City': city,
            'Country': country,
            'IATA': iata,
            'ICAO': icao,
            'Latitudine': latitudine,
            'Longitudine': longitudine,
            'Altitude': altitude,
            'Timezone': timezone,
            'DST': dst,
            'Tz database time zone': tz_database_timezone,
            'Type': type,
            'Source': source
        }
        result = self.airports_collection.insert_one(airport)
        airport['_id'] = result.inserted_id
        return airport

    def update_airport(self, airport_id, name=None, city=None, country=None, iata=None, icao=None,
                       latitudine=None, longitudine=None, altitude=None, timezone=None, dst=None,
                       tz_database_timezone=None, type=None, source=None):
        update_fields = {}
        if airport_id:
            update_fields['Airport ID'] = airport_id
        if name:
            update_fields['Name'] = name
        if city:
            update_fields['City'] = city
        if country:
            update_fields['Country'] = country
        if iata:
            update_fields['IATA'] = iata
        if icao:
            update_fields['ICAO'] = icao
        if latitudine:
            update_fields['Latitudine'] = latitudine
        if longitudine:
            update_fields['Longitudine'] = longitudine
        if altitude:
            update_fields['Altitude'] = altitude
        if timezone:
            update_fields['Timezone'] = timezone
        if dst:
            update_fields['DST'] = dst
        if tz_database_timezone:
            update_fields['Tz database time zone'] = tz_database_timezone
        if type:
            update_fields['Type'] = type
        if source:
            update_fields['Source'] = source

        result = self.airports_collection.find_one_and_update(
            {'_id': ObjectId(airport_id)},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def delete_airport(self, airport_id):
        result = self.airports_collection.delete_one({'_id': ObjectId(airport_id)})
        return result.deleted_count > 0

    def get_cities_with_most_airports(self):
        pipeline = [
            {"$match": {"City": {"$ne": None}}},  # Filtro per escludere città con valore null
            {"$group": {"_id": "$City", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1000}
        ]
        return list(self.airports_collection.aggregate(pipeline))


