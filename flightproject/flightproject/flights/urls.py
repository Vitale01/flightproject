from django.urls import path
from . import views

urlpatterns = [
    path('frequent-flights/', views.frequent_flights, name='frequent_flights'),
]
