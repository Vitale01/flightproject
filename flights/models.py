# flights/models.py
import uuid

from djongo import models


class Route(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=255)
    icao_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airport(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    airport_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iata = models.CharField(max_length=255)
    icao = models.CharField(max_length=255)
    latitudine = models.DecimalField(max_digits=10, decimal_places=2)
    longitudine = models.DecimalField(max_digits=10, decimal_places=2)
    altitude = models.DecimalField(max_digits=10, decimal_places=2)
    timezone = models.CharField(max_length=255)
    dst = models.CharField(max_length=255)
    tz_database_timezone = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.name
