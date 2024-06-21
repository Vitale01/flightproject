# flights/models.py

from djongo import models

class Route(models.Model):
    id = models.IntegerField(primary_key=True)
    airline = models.CharField(max_length=255)
    airline_id = models.CharField(max_length=255)
    source_airport = models.CharField(max_length=255)
    source_airport_id = models.CharField(max_length=255)
    destination_airport = models.CharField(max_length=255)
    destination_airport_id = models.CharField(max_length=255)
    stops = models.IntegerField()
    equipment = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.airline} ({self.source_airport} -> {self.destination_airport})"

class Airline(models.Model):
    id = models.IntegerField(primary_key=True)
    airline_id = models.IntegerField()
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    iata = models.CharField(max_length=255)
    callsign = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    active = models.CharField(max_length=255)
    icao = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Airplane(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=255)
    icao_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Airport(models.Model):
    id = models.IntegerField(primary_key=True)
    airport_id = models.IntegerField()
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iata = models.CharField(max_length=255)
    icao = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    timezone = models.CharField(max_length=255)
    dst = models.CharField(max_length=255)
    db_timezone = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.name
