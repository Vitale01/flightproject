from pymongo import MongoClient

# Connettersi a MongoDB
client = MongoClient('localhost', 27017)
db = client['Voli']

# Funzione per ottenere un esempio di documento e i suoi tipi di dati
def print_collection_schema(collection_name):
    collection = db[collection_name]
    document = collection.find_one()
    if document:
        print(f"Schema for collection '{collection_name}':")
        for key, value in document.items():
            print(f" - {key}: {type(value).__name__}")
    else:
        print(f"No documents found in collection '{collection_name}'")

# Liste delle collezioni da esaminare
collections = ['airlines', 'airplanes', 'airport', 'routes']

# Stampare gli schemi delle collezioni
for collection_name in collections:
    print_collection_schema(collection_name)
    print()

client.close()
