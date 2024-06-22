from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Route, Airline, Airport, Airplane

admin.site.register(Route)
admin.site.register(Airplane)
admin.site.register(Airline)
admin.site.register(Airport)
