# flights/load_data.py

import pandas as pd
from flightproject.flights.models import Airline, Airplane, Flight


def load_data():
    airlines_df = pd.read_csv('airlines.csv')
    airplanes_df = pd.read_csv('airplanes.csv')
    flights_df = pd.read_csv('flights.csv')

    for _, row in airlines_df.iterrows():
        Airline.objects.create(id=row['id'], name=row['name'], country=row['country'])

    for _, row in airplanes_df.iterrows():
        Airplane.objects.create(id=row['id'], model=row['model'], capacity=row['capacity'])

    for _, row in flights_df.iterrows():
        Flight.objects.create(flight_number=row['flight_number'], airline=row['airline'],
                              destination=row['destination'], departure_date=row['departure_date'])
